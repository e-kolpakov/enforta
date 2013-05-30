#-*- coding: utf-8 -*-
import json
import logging

from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView, DetailView
from django.contrib import messages

from guardian.decorators import permission_required
from DocApproval.request_management.actions import RequestActionRepository
from DocApproval.request_management.request_factory import RequestFactory

from ..menu import RequestContextMenuManagerExtension, MenuModifierViewMixin
from ..messages import CommonMessages, RequestMessages
from ..models import Request, RequestStatus, Permissions
from ..url_naming.names import Request as RequestUrl, Profile as ProfileUrl
from ..forms import EditRequestForm, EditContractForm

from ..utilities.utility import get_url_base, reprint_form_errors
from ..utilities.datatables import JsonConfigurableDatatablesBaseView


class CreateUpdateRequestView(TemplateView):
    _logger = logging.getLogger(__name__)

    override_request_status = None
    template_name = None

    request_form_class = None
    contract_form_class = None

    form_heading = None
    form_submit = None

    success_message = None

    def get_instances(self, pk):
        raise NotImplementedError()

    def get_return_url(self, pk):
        raise NotImplementedError()

    def get_initial_request(self, request, *args, **kwargs):
        return {}

    def get_initial_contract(self, request, *args, **kwargs):
        return {}

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
            'form_heading': self.form_heading,
            'form_submit': self.form_submit,
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
            self._logger.error(u"Error saving the request:\n{0}".format(u"\n".join(errors)))
            return render(request, self.template_name, {
                'request_form': request_form,
                'contract_form': contract_form,
                'return_url': self.get_return_url(pk)
            })


# Permission protection is on the base class
class CreateRequestView(CreateUpdateRequestView):
    _logger = logging.getLogger(__name__)

    request_form_class = EditRequestForm
    contract_form_class = EditContractForm
    template_name = 'request/edit.html'

    form_heading = RequestMessages.CREATE_REQUEST
    form_submit = CommonMessages.CREATE

    override_request_status = RequestStatus.PROJECT
    success_message = RequestMessages.REQUEST_CREATED

    @method_decorator(permission_required(Permissions._(Permissions.Request.CAN_CREATE_REQUESTS), raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(CreateUpdateRequestView, self).dispatch(request, *args, **kwargs)

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
    _logger = logging.getLogger(__name__)

    request_form_class = EditRequestForm
    contract_form_class = EditContractForm
    template_name = 'request/edit.html'
    extender_class = RequestContextMenuManagerExtension

    form_heading = RequestMessages.MODIFY_REQUEST
    form_submit = CommonMessages.MODIFY
    success_message = RequestMessages.REQUEST_MODIFIED

    @method_decorator(permission_required(
        Permissions._(Permissions.Request.CAN_EDIT_REQUEST),
        (Request, 'pk', 'pk'),
        return_403=True)
    )
    def dispatch(self, request, *args, **kwargs):
        return super(CreateUpdateRequestView, self).dispatch(request, *args, **kwargs)

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

    def _get_actions(self, user, request):
        """ request is an instance of models.Request here"""
        return [
            action
            for key, action in RequestActionRepository().items()
            if action.is_available(user, request)
        ]

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
            'contract': contract,
            'actions': self._get_actions(request.user, req),
            'actions_backend_url': reverse(RequestUrl.ACTIONS_BACKEND_JSON)
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
        show_only = self.request.GET.get('show_only', None)
        qs = self.model.objects.get_accessible_requests(self.request.user)
        if show_only == ListRequestView.MY_APPROVALS:
            qs = self.model.objects.get_awaiting_approval(self.request.user)
        elif show_only == ListRequestView.MY_REQUESTS:
            pass
        return qs

    def filter_queryset(self, qs):
        sSearch = self.request.GET.get('sSearch', None)
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


class RequestActionsJson(View):
    _logger = logging.getLogger(__name__)

    def _parse_parameters(self, request):
        if request.is_ajax():
            raw_data = request.body
            data = json.loads(raw_data)
            return {
                'action': data.get('action', None),
                'request_pk': data.get('request_pk', None),
                'parameters': data.get('parameters', {})
            }
        else:
            raise ValueError("Data should be json-formatted")

    def post(self, request, *args, **kwargs):
        try:
            parsed_parameters = self._parse_parameters(request)
            action = RequestActionRepository()[parsed_parameters['action']]
            req = Request.objects.get(pk=parsed_parameters['request_pk'])

            if action.is_available(request.user, req):
                params = parsed_parameters['parameters']
                response = action.execute(request.user, req, **params)
            else:
                response = RequestMessages.ACTION_IS_NOT_ACCESSIBLE

            data = {
                'success': True,
                'response': response
            }
        except Exception as e:
            self._logger.exception(e.message)
            data = {
                'success': False,
                'response': None,
                'errors': [e.message]
            }
        return HttpResponse(json.dumps(data), content_type="application/json")


def archive(request, year=None, month=None):
    return render(request, "request/archive.html", {'year': year, 'month': month})