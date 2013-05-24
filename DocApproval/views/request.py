#-*- coding: utf-8 -*-
import logging

from django.core.urlresolvers import reverse
from django.shortcuts import (render, HttpResponseRedirect, get_object_or_404)
from django.utils.decorators import method_decorator
from django.views.generic import (TemplateView, DetailView)
from django.contrib import messages

from guardian.decorators import permission_required

from ..menu import RequestContextMenuManagerExtension, MenuModifierViewMixin
from ..messages import CommonMessages, RequestMessages
from ..models import (Request, RequestStatus, Permissions, RequestFactory)
from ..url_naming.names import (Request as RequestUrl, Profile as ProfileUrl)
from ..forms import (CreateRequestForm, CreateContractForm, UpdateRequestForm, UpdateContractForm)

from ..utilities.utility import (get_url_base, reprint_form_errors)
from ..utilities.datatables import JsonConfigurableDatatablesBaseView

logger = logging.getLogger(__name__)


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

    @method_decorator(permission_required(Permissions._(Permissions.Request.CAN_CREATE_REQUESTS), raise_exception=True))
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
        create_handler = RequestFactory(request_form, contract_form, request.user)

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


# Permission protection is on the base class
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


# Permission protection is on the base class
class UpdateRequestView(CreateUpdateRequestView, MenuModifierViewMixin):
    request_form_class = UpdateRequestForm
    contract_form_class = UpdateContractForm
    template_name = 'request/update.html'
    extender_class = RequestContextMenuManagerExtension

    success_message = RequestMessages.REQUEST_MODIFIED

    def get_instances(self, pk):
        request = get_object_or_404(Request, pk=pk)
        return request, request.contract

    def get_return_url(self, pk):
        return reverse(RequestUrl.DETAILS, kwargs={'pk': int(pk)})

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', 0)
        request_instance, contract_instance = self.get_instances(pk)
        if request_instance:
            self._apply_extender(request, request_instance)
        return super(UpdateRequestView, self).get(request, *args, **kwargs)


class ListRequestView(TemplateView):
    SHOW_ONLY_PARAM = 'show_only'
    MY_REQUESTS = 'my_requests'
    MY_APPROVALS = 'my_approvals'

    template_name = 'request/list.html'

    def get(self, request, *args, **kwargs):
        show_only = kwargs.get(self.SHOW_ONLY_PARAM, None)
        return render(request, self.template_name, {
            'datatables_data': RequestUrl.LIST_JSON,
            'datatables_config': RequestUrl.LIST_JSON_CONF,
            'show_only': show_only
        })


class DetailRequestView(DetailView, MenuModifierViewMixin):
    template_name = 'request/details.html'
    _logger = logging.getLogger(__name__)
    extender_class = RequestContextMenuManagerExtension

    @method_decorator(permission_required(
        Permissions._(Permissions.Request.CAN_VIEW_REQUEST),
        (Request, 'pk', 'pk'),
        return_403=True)
    )
    def dispatch(self, request, *args, **kwargs):
        return super(DetailRequestView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        pk = kwargs.get(self.pk_url_kwarg, None)
        exclude_fields = ['id', 'contract']
        req = get_object_or_404(Request, pk=pk)
        self._apply_extender(request, req)

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
    model_fields = ('name', 'city', 'status', 'creator', 'send_on_approval', 'created', 'accepted')
    calculated_fields = {'current_approvers': RequestMessages.CURRENT_REVIEVERS, }

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
        show_only = self.request.POST.get('show_only', None)
        if show_only == ListRequestView.MY_APPROVALS:
            qs = self.model.objects.get_awaiting_approval(self.request.user)
        elif show_only == ListRequestView.MY_REQUESTS or show_only is None:
            qs = self.model.objects.get_accessible_requests(self.request.user)

        # sSearch = self.request.POST.get('sSearch', None)
        # if sSearch:
        #     qs = qs.filter(name__istartswith=sSearch)
        return qs

    def filter_queryset(self, qs):
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
            'creator_pk': item.creator.pk,
            'current_approvers': [profile.get_short_name() for profile in item.approval_route.get_current_reviewers()]
        }


def archive(request, year=None, month=None):
    return render(request, "request/archive.html", {'year': year, 'month': month})