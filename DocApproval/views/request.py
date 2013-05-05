#-*- coding: utf-8 -*-
import logging
from django.contrib.auth.decorators import permission_required

from django.db import transaction
from django.core.urlresolvers import reverse
from django.shortcuts import (render, HttpResponseRedirect, get_object_or_404)
from django.utils.decorators import method_decorator
from django.views.generic import (TemplateView, DetailView)
from django.contrib import messages
from DocApproval.menu import RequestContextMenuManagerExtension

from ..models import (Request, RequestStatus, Permissions)
from ..forms import (CreateRequestForm, CreateContractForm, UpdateRequestForm, UpdateContractForm)
from ..url_naming.names import (Request as RequestUrl, Profile as ProfileUrl)
from ..messages import CommonMessages, RequestMessages

from ..utilities.utility import (get_url_base, reprint_form_errors)
from ..utilities.datatables import JsonConfigurableDatatablesBaseView

logger = logging.getLogger(__name__)


class RequestCreateUpdateHandler(object):
    def __init__(self, request_form, contract_form, user_profile):
        self._req_form = request_form
        self._con_form = contract_form
        self._user_profile = user_profile

    @transaction.commit_on_success
    def persist_request(self, override_status=None):
        new_request = self._req_form.save(commit=False)
        if override_status:
            new_request.status = RequestStatus.objects.get(pk=override_status)
        new_request.creator = self._user_profile
        new_request.last_updater = self._user_profile

        new_request.contract = self._con_form.save()
        new_request.save()

        return new_request


class CreateUpdateRequestView(TemplateView):
    override_request_status = None
    template_name = None

    request_form_class = None
    contract_form_class = None

    success_message = None

    def get_instances(self, pk):
        raise NotImplementedError()

    def get_return_url(self, pk):
        raise NotImplementedError()

    def get_initial_request(self, request, *args, **kwargs):
        return {}

    def get_initial_contract(self, request, *args, **kwargs):
        return {}

    @method_decorator(permission_required(Permissions.Request.CAN_CREATE_REQUESTS, raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(CreateUpdateRequestView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', 0)
        request_instance, contract_instance = self.get_instances(pk)
        request_initial = self.get_initial_request(request, *args, **kwargs)
        contract_initial = self.get_initial_contract(request, *args, **kwargs)
        request_form = self.request_form_class(instance=request_instance, initial=request_initial, prefix='request')
        contract_form = self.contract_form_class(instance=contract_instance, initial=contract_initial,
                                                 prefix='contract')
        return render(request, self.template_name, {
            'request_form': request_form,
            'contract_form': contract_form,
            'return_url': self.get_return_url(pk)
        })

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', 0)
        request_instance, contract_instance = self.get_instances(pk)
        request_form = self.request_form_class(request.POST, instance=request_instance, prefix='request')
        contract_form = self.contract_form_class(request.POST, request.FILES, instance=contract_instance,
                                                 prefix='contract')
        create_handler = RequestCreateUpdateHandler(request_form, contract_form, request.user.profile)

        if request_form.is_valid() and contract_form.is_valid():
            new_request = create_handler.persist_request(override_status=self.override_request_status)
            messages.success(request, self.success_message)
            return HttpResponseRedirect(reverse(RequestUrl.DETAILS, kwargs={'pk': new_request.pk}))
        else:
            messages.error(request, CommonMessages.FORM_VALIDATION_ERROR)
            errors = reprint_form_errors(request_form.errors) + reprint_form_errors(contract_form.errors)
            logger.error(u"Error saving the request:\n{0}".format(u"\n".join(errors)))
            return render(request, self.template_name, {
                'request_form': request_form,
                'contract_form': contract_form,
                'return_url': self.get_return_url(pk)
            })


class CreateRequestView(CreateUpdateRequestView):
    request_form_class = CreateRequestForm
    contract_form_class = CreateContractForm
    template_name = 'request/create.html'

    override_request_status = RequestStatus.PROJECT
    success_message = RequestMessages.REQUEST_CREATED

    def get_instances(self, pk):
        return None, None

    def get_initial_request(self, request, *args, **kwargs):
        return {}

    def get_initial_contract(self, request, *args, **kwargs):
        return {}

    def get_return_url(self, pk):
        return reverse(RequestUrl.LIST)


class UpdateRequestView(CreateUpdateRequestView):
    request_form_class = UpdateRequestForm
    contract_form_class = UpdateContractForm
    template_name = 'request/update.html'

    success_message = RequestMessages.REQUEST_MODIFIED

    def get_instances(self, pk):
        request = get_object_or_404(Request, pk=pk)
        return request, request.contract

    def get_return_url(self, pk):
        return reverse(RequestUrl.DETAILS, kwargs={'pk': int(pk)})


class ListRequestView(TemplateView):
    SHOW_ONLY_PARAM = 'show_only'
    MY_REQUESTS = 'my_requests'
    MY_APPROVALS = 'my_approvals'

    template_name = 'request/list.html'
    logger = logging.getLogger(__name__)

    def get(self, request, *args, **kwargs):
        show_only = kwargs.get(self.SHOW_ONLY_PARAM, None)
        return render(request, self.template_name, {
            'datatables_data': RequestUrl.LIST_JSON,
            'datatables_config': RequestUrl.LIST_JSON_CONF,
            'show_only': show_only
        })


class DetailRequestView(DetailView):
    template_name = 'request/details.html'
    _logger = logging.getLogger(__name__)

    def _modify_menu(self, request, request_id, allow_edit):
        RequestContextMenuManagerExtension(request, allow_edit).extend(request_id)

    def _report_error(self, request, request_id, user_message, log_message):
        messages.error(request, user_message)
        self._logger.warning(log_message, {'id': request_id, 'username': request.user.username})

    def get(self, request, *args, **kwargs):
        pk = kwargs.get(self.pk_url_kwarg, None)
        exclude_fields = ['id', 'contract']
        try:
            req = Request.objects.get(pk=pk)
            self._modify_menu(request, pk, req.accessible_by(request.user))
            if not req.accessible_by(request.user):
                req = None
                self._report_error(request, pk, RequestMessages.ACCESS_DENIED,
                                   "User {username} does not have access to request {id}")
        except Request.DoesNotExist:
            req = None
            self._report_error(request, pk, RequestMessages.DOES_NOT_EXIST, "Request {id} does not exist")

        if req and not req.accepted:
            exclude_fields.append('accepted')

        contract = req.contract if req else None

        return render(request, self.template_name, {
            'doc_request': req,
            'exclude_fields_req': exclude_fields,
            'contract': contract
        })


class RequestListJson(JsonConfigurableDatatablesBaseView):
    model = Request
    link_field = 'name'
    display_fields = ('name', 'city', 'status', 'creator', 'send_on_approval', 'created', 'accepted')

    def get_links_config(self):
        return {
            'name': {
                'base_url': get_url_base(reverse(RequestUrl.DETAILS, kwargs={'pk': 0}))
            },
            'send_on_approval': {
                'base_url': get_url_base(reverse(ProfileUrl.PROFILE, kwargs={'pk': 0})),
                'entity_key': 'send_on_approval_pk',
            },
            'creator': {
                'base_url': get_url_base(reverse(ProfileUrl.PROFILE, kwargs={'pk': 0})),
                'entity_key': 'creator_pk',
            }
        }

    def get_initial_queryset(self):
        return self.model.objects.get_accessible_requests(self.request.user)

    def filter_queryset(self, qs):
        show_only = self.request.POST.get('show_only', None)
        if show_only == ListRequestView.MY_APPROVALS:
            qs = self.get_initial_queryset()
        elif show_only == ListRequestView.MY_REQUESTS:
            qs = self.get_initial_queryset()

        sSearch = self.request.POST.get('sSearch', None)
        if sSearch:
            qs = qs.filter(name__istartswith=sSearch)
        return qs

    def prepare_single_item(self, item):
        accepted = item.accepted.strftime("%Y-%m-%d") if item.accepted is not None else "---"
        return {
            'pk': item.pk,
            'name': item.name,
            'city': item.city.city_name,
            'status': item.status.status_name,
            'creator': item.creator.get_full_name(),
            'send_on_approval': item.send_on_approval.get_full_name(),
            'created': item.created.strftime("%Y-%m-%d"),
            'accepted': accepted,
            'send_on_approval_pk': item.send_on_approval.pk,
            'creator_pk': item.creator.pk
        }


def archive(request, year=None, month=None):
    return render(request, "request/archive.html", {'year': year, 'month': month})