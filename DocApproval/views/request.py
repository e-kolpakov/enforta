#-*- coding: utf-8 -*-
import logging
from django.contrib.auth.decorators import permission_required, login_required

from django.core.urlresolvers import reverse
from django.shortcuts import (render, HttpResponseRedirect)
from django.utils.decorators import method_decorator
from django.views.generic import (TemplateView, UpdateView, CreateView, DetailView)
from django.contrib import messages

from ..models import (Request, RequestStatus, UserProfile, Permissions)
from ..forms import (CreateRequestForm, CreateContractForm)
from ..url_naming.names import (Request as RequestUrl, Profile as ProfileUrl)
from ..messages import RequestMessages

from ..extensions.utility import (get_url_base, reprint_form_errors)
from ..extensions.datatables import JsonConfigurableDatatablesBaseView

logger = logging.getLogger(__name__)


class CreateRequestView(CreateView):
    request_form_class = CreateRequestForm
    contract_form_class = CreateContractForm
    template_name = 'request/create.html'

    @method_decorator(permission_required(Permissions.Request.CAN_CREATE_REQUESTS, raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(CreateRequestView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # TODO: add initialization of defaults, e.g. city, approver, etc.
        request_form = self.request_form_class(initial={}, prefix='request')
        contract_form = self.contract_form_class(initial={}, prefix='contract')
        return render(request, self.template_name, {'request_form': request_form, 'contract_form':contract_form})

    def post(self, request, *args, **kwargs):
        request_form = self.request_form_class(request.POST, prefix='request')
        contract_form = self.contract_form_class(request.POST, request.FILES, prefix='contract')
        if request_form.is_valid() and contract_form.is_valid():
            contract = contract_form.save()

            new_request = request_form.save(commit=False)
            new_request.status = RequestStatus.objects.get(pk=RequestStatus.PROJECT)
            new_request.creator = request.user.profile
            new_request.last_updater = request.user.profile

            new_request.contract = contract
            new_request.save()
            messages.success(request, RequestMessages.REQUEST_CREATED)
            return HttpResponseRedirect(reverse(RequestUrl.DETAILS, kwargs={'pk': new_request.pk}))
        else:
            messages.error(request, RequestMessages.REQUEST_CREATION_ERROR)
            errors = reprint_form_errors(request_form.errors) + reprint_form_errors(contract_form.errors)
            logger.error(u"Error saving the request:\n{0}".format(u"\n".join(errors)))
        return render(request, self.template_name, {'request_form': request_form, 'contract_form': contract_form})


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


class UpdateRequestView(UpdateView):
    template_name = 'request/update.html'
    model = Request


class DetailRequestView(DetailView):
    template_name = 'request/details.html'
    _logger = logging.getLogger(__name__)

    def _report_error(self, request, request_id, user_message, log_message):
        messages.error(request, user_message)
        self._logger.warning(log_message, {'id': request_id, 'username': request.user.username})

    def get(self, request, *args, **kwargs):
        pk = kwargs.get(self.pk_url_kwarg, None)
        exclude_fields = ['id', 'document']
        # self._modify_menu(request, user_id, allow_edit)
        try:
            req = Request.objects.get(pk=pk)
            if not req.accessible_by(request.user):
                req = None
                self._report_error(request, pk, RequestMessages.ACCESS_DENIED,
                                   "User {username} does not have access to request {id}")
        except Request.DoesNotExist:
            req = None
            self._report_error(request, pk, RequestMessages.DOES_NOT_EXIST, "Request {id} does not exist")

        if req and not req.accepted:
                exclude_fields.append('accepted')

        return render(request, self.template_name, {
            'doc_request': req,
            'exclude_fields_req': exclude_fields,
            'contract': req.contract
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