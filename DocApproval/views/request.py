#-*- coding: utf-8 -*-
import json
import logging

from django.core.urlresolvers import reverse
from django.db.models.expressions import F
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView, DetailView, ListView
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages

from DocApproval.constants import Groups
from DocApproval.forms import EditRequestForm, EditContractForm
from DocApproval.messages import CommonMessages, RequestMessages
from DocApproval.menu import RequestContextMenuManagerExtension, MenuModifierViewMixin
from DocApproval.models import Request, RequestStatus, Permissions, City, UserProfile, RequestHistory
from DocApproval.request_management import actions as request_actions, request_factory
from DocApproval.url_naming.names import Request as RequestUrl, Profile as ProfileUrl, ApprovalRoute as ApprovalRouteUrls

from DocApproval.utilities.datatables import JsonConfigurableDatatablesBaseView, LinkColumnDefinition, ColumnDefinition, ActionsColumnDefintion
from DocApproval.utilities.permission_checker import impersonated_permission_required
from DocApproval.utilities.utility import get_url_base, reprint_form_errors, parse_string_to_datetime


class CreateUpdateRequestView(TemplateView):
    _logger = logging.getLogger(__name__)

    override_request_status = None
    template_name = None

    request_form_class = None
    contract_form_class = None

    form_heading = None
    form_submit = None

    success_message = None
    redirect_on_success = None

    def get_instances(self, pk):
        raise NotImplementedError()

    def get_return_url(self, pk):
        raise NotImplementedError()

    def get_initial_request(self, request, *args, **kwargs):
        return {}

    def get_initial_contract(self, request, *args, **kwargs):
        return {}

    def _build_render_context(self, pk, request_form, contract_form):
        return {
            'request_form': request_form,
            'contract_form': contract_form,
            'form_heading': self.form_heading,
            'form_submit': self.form_submit,
            'return_url': self.get_return_url(pk)
        }

    def redirect_on_success(self, request):
        raise NotImplementedError()

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', 0)
        request_instance, contract_instance = self.get_instances(pk)
        if request_instance and not request_instance.editable:
            messages.warning(request, RequestMessages.ONLY_PROJECT_REQUESTS_EDITABLE)
            return HttpResponseRedirect(reverse(RequestUrl.DETAILS, kwargs={'pk': request_instance.pk}))
        request_form = self.request_form_class(
            instance=request_instance,
            initial=self.get_initial_request(request, *args, **kwargs),
            prefix='request'
        )
        contract_form = self.contract_form_class(
            instance=contract_instance,
            initial=self.get_initial_contract(request, *args, **kwargs),
            prefix='contract'
        )
        return render(request, self.template_name, self._build_render_context(pk, request_form, contract_form))


    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', 0)
        request_instance, contract_instance = self.get_instances(pk)
        request_form = self.request_form_class(request.POST, instance=request_instance, prefix='request')
        contract_form = self.contract_form_class(request.POST, request.FILES, instance=contract_instance,
                                                 prefix='contract')
        create_handler = request_factory.RequestFactory(request_form, contract_form, request.user)

        if request_form.is_valid() and contract_form.is_valid():
            new_request = create_handler.persist_request(override_status=self.override_request_status)
            messages.success(request, self.success_message)
            return HttpResponseRedirect(self.redirect_on_success(new_request))
        else:
            messages.error(request, CommonMessages.FORM_VALIDATION_ERROR)
            errors = reprint_form_errors(request_form.errors) + reprint_form_errors(contract_form.errors)
            self._logger.error(u"Error saving the request:\n{0}".format(u"\n".join(errors)))
            return render(request, self.template_name, self._build_render_context(pk, request_form, contract_form))


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

    def redirect_on_success(self, request):
        return reverse(ApprovalRouteUrls.UPDATE, kwargs={'pk': request.approval_route.pk})

    @method_decorator(impersonated_permission_required(
        class_permissions=Permissions.Request.CAN_CREATE_REQUESTS,
        return_403=True
    ))
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

    def redirect_on_success(self, request):
        return reverse(RequestUrl.DETAILS, kwargs={'pk': request.pk})

    @method_decorator(impersonated_permission_required(
        class_permissions=Permissions.Request.CAN_VIEW_ALL_REQUESTS,
        instance_permissions=Permissions.Request.CAN_EDIT_REQUEST,
        lookup_variables=(Request, 'pk', 'pk'),
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


class DetailRequestView(DetailView, MenuModifierViewMixin):
    template_name = 'request/details.html'
    _logger = logging.getLogger(__name__)
    extender_class = RequestContextMenuManagerExtension

    @method_decorator(impersonated_permission_required(
        class_permissions=Permissions.Request.CAN_VIEW_ALL_REQUESTS,
        instance_permissions=Permissions.Request.CAN_VIEW_REQUEST,
        lookup_variables=(Request, 'pk', 'pk'),
        return_403=True)
    )
    def dispatch(self, request, *args, **kwargs):
        return super(DetailRequestView, self).dispatch(request, *args, **kwargs)

    def _get_actions(self, user, request):
        """ request is an instance of models.Request here"""
        return [
            action
            for key, action in request_actions.RequestActionRepository().items()
            if action.is_available(user, request)
        ]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get(self.pk_url_kwarg, None)
        exclude_fields = ['id', 'contract', 'approval_route']
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
            'actions_backend_url': reverse(RequestUrl.ACTIONS_BACKEND_JSON),
            'show_approval_process': req.show_process,
            'approval_process_url': reverse(RequestUrl.APPROVAL_PROCESS, kwargs={'pk': req.approval_route.pk})
        })


class RequestApprovalProcessView(DetailView, SingleObjectMixin):
    template_name = 'request/details.html'
    _logger = logging.getLogger(__name__)
    extender_class = RequestContextMenuManagerExtension

    @method_decorator(impersonated_permission_required(
        class_permissions=Permissions.Request.CAN_VIEW_ALL_REQUESTS,
        instance_permissions=Permissions.Request.CAN_VIEW_REQUEST,
        lookup_variables=(Request, 'pk', 'pk'),
        return_403=True)
    )
    def dispatch(self, request, *args, **kwargs):
        return super(RequestApprovalProcessView, self).dispatch(request, *args, **kwargs)


class ListRequestView(TemplateView):
    SHOW_ONLY_PARAM = 'show_only'
    MY_REQUESTS = 'my_requests'
    MY_APPROVALS = 'my_approvals'

    template_name = 'request/list.html'

    def _get_filter_data(self):
        return {
            'cities': City.objects.all(),
            'statuses': RequestStatus.objects.all(),
            'users': UserProfile.get_users_in_group(Groups.USERS),
            'approvers': UserProfile.get_users_in_group(Groups.APPROVERS)
        }

    def get(self, request, *args, **kwargs):
        show_only = kwargs.get(self.SHOW_ONLY_PARAM, None)
        return render(request, self.template_name, {
            'datatables_data': RequestUrl.LIST_JSON,
            'datatables_config': RequestUrl.LIST_JSON_CONF,
            'show_only': show_only,
            'filter_data': self._get_filter_data()
        })


class RequestHistoryView(SingleObjectMixin, ListView, MenuModifierViewMixin):
    AUTO_FILTER_TOKEN = 'auto_filter'
    APPROVE_ACTIONS_ONLY = 'approve_actions_only'

    paginate_by = 50
    template_name = "request/request_approval_history.html"
    _logger = logging.getLogger(__name__)
    extender_class = RequestContextMenuManagerExtension

    def get_context_data(self, **kwargs):
        kwargs['request'] = self.object
        return super(RequestHistoryView, self).get_context_data(**kwargs)

    def get_queryset(self):
        result = RequestHistory.objects.filter(request=self.object).order_by('action_date')
        if self.auto_filter and self.auto_filter == self.APPROVE_ACTIONS_ONLY:
            result = result.filter(action_type__in=RequestHistory.approval_actions)
        return result

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(Request.objects.all())
        self.auto_filter = kwargs.get(self.AUTO_FILTER_TOKEN, None)
        self._apply_extender(request, self.object)
        return super(RequestHistoryView, self).get(request, *args, **kwargs)


class RequestListJson(JsonConfigurableDatatablesBaseView):
    model = Request
    model_fields = ('name', 'city', 'status', 'creator', 'send_on_approval', 'created', 'accepted')

    as_is = lambda x: x
    to_date = parse_string_to_datetime

    _search_criteria = {
        'name': {'lookup': 'name__istartswith', 'converter': as_is},
        'status': {'lookup': 'status__code', 'converter': as_is},
        'date_created_from': {'lookup': 'created__gte', 'converter': to_date},
        'date_created_to': {'lookup': 'created__lte', 'converter': to_date},
        'date_accepted_from': {'lookup': 'accepted__gte', 'converter': to_date},
        'date_accepted_to': {'lookup': 'accepted__lte', 'converter': to_date},
        'creator': {'lookup': 'creator__pk', 'converter': int},
        'city': {'lookup': 'city', 'converter': int},
        'current_approver': {
            'Q_gen': lambda approver: (
                Q(approval_route__processes__is_current=True) &
                Q(approval_route__processes__is_successful=False) &
                Q(approval_route__steps__step_number=F('approval_route__processes__current_step_number')) &
                Q(approval_route__steps__approver__in=UserProfile.objects.get(pk=approver).effective_profiles)
            ),
            'converter': int
        },
    }

    def get_other_columns(self):
        rslt = {
            # 'checkboxes': CheckboxColumnDefinition(entity_key='pk', order=-1),
            'name': LinkColumnDefinition(
                field='name', model=self.model,
                base_url=get_url_base(reverse(RequestUrl.DETAILS, kwargs={'pk': 0})),
                order=0
            ),
            'send_on_approval': LinkColumnDefinition(
                field='send_on_approval', model=self.model,
                base_url=get_url_base(reverse(ProfileUrl.PROFILE, kwargs={'pk': 0})),
                entity_key='send_on_approval_pk', order=1000
            ),
            'creator': LinkColumnDefinition(
                field='creator', model=self.model,
                base_url=get_url_base(reverse(ProfileUrl.PROFILE, kwargs={'pk': 0})),
                entity_key='creator_pk', order=1001
            ),
            'current_approvers': ColumnDefinition(
                column='current_approvers',
                name=RequestMessages.CURRENT_REVIEVERS,
                is_calculated=True, order=1002
            )
        }
        if self.request.GET.get('show_only', None) == ListRequestView.MY_APPROVALS:
            action_repository = request_actions.RequestActionRepository()
            rslt['actions'] = ActionsColumnDefintion(
                actions=[
                    action_repository[request_actions.RequestActionRepository.APPROVE],
                    action_repository[request_actions.RequestActionRepository.REJECT]
                ],
                backend_url=reverse(RequestUrl.ACTIONS_BACKEND_JSON),
                order=-2
            )
        return rslt

    def get_initial_queryset(self):
        show_only = self.request.GET.get('show_only', None)

        if show_only == ListRequestView.MY_APPROVALS:
            qs = self.model.objects.get_awaiting_approval(self.request.user)
        elif show_only == ListRequestView.MY_REQUESTS:
            qs = self.model.objects.get_accessible_requests(self.request.user)
        else:
            qs = self.model.objects.get_accessible_requests(self.request.user)
        return qs

    def filter_queryset(self, qs):
        filters = {}
        q_lookups = []
        for parameter, parameter_mapping in self._search_criteria.items():
            val = self.request.GET.get(parameter, None)
            if val is not None:
                if 'lookup' in parameter_mapping:
                    filters[parameter_mapping['lookup']] = parameter_mapping['converter'](val)
                elif 'Q_gen' in parameter_mapping:
                    q_lookups.append(parameter_mapping['Q_gen'](val))

        if filters or q_lookups:
            qs = qs.filter(*q_lookups, **filters)
        return qs.select_related('city', 'creator', 'status', 'send_on_approval')

    def prepare_single_item(self, item):
        accepted = item.accepted.strftime("%Y-%m-%d") if item.accepted is not None else "---"
        return {
            'pk': item.pk,
            'name': item.name,
            'city': item.city.name,
            'status': item.status.name,
            'creator': item.creator.full_name,
            'send_on_approval': item.send_on_approval.full_name,
            'created': item.created.strftime("%Y-%m-%d"),
            'accepted': accepted,
            'send_on_approval_pk': item.send_on_approval.pk,
            'creator_pk': item.creator.pk,
            'current_approvers': ", ".join(profile.short_name for profile in item.get_current_approvers())
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
            action = request_actions.RequestActionRepository()[parsed_parameters['action']]
            req = Request.objects.get(pk=parsed_parameters['request_pk'])

            if action.is_available(request.user, req):
                params = parsed_parameters['parameters']
                response = action.execute(request.user, req, **params)
            else:
                response = RequestMessages.ACTION_IS_NOT_ACCESSIBLE.format(req)

            data = {
                'success': True,
                'response': response
            }
        except Exception as e:
            self._logger.exception(e)
            data = {
                'success': False,
                'response': None,
                'errors': [e.message]
            }
        return HttpResponse(json.dumps(data), content_type="application/json")


def archive(request, year=None, month=None):
    return render(request, "request/archive.html", {'year': year, 'month': month})