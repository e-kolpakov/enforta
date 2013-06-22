# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.views.generic import TemplateView

from DocApproval.models import Groups, Request, RequestStatus


class HomePagePartBase(object):
    show_to_groups = ()
    template = None
    code = None
    rows_limit = 20

    def __init__(self, request):
        self.request = request

    def should_show(self, user, user_groups):
        return set(user_groups) & set(self.show_to_groups)

    @property
    def data(self):
        return None


class MyApprovalsHomePagePart(HomePagePartBase):
    show_to_groups = (Groups.APPROVERS, )
    template = "home_page/generic_request_list_page.html"
    code = 'my_approvals'
    label = _(u"Ожидают утверждения")
    no_rows = _(u"Нет заявок требующих утверждения")

    @property
    def data(self):
        return Request.objects.get_awaiting_approval(self.request.user).order_by('created')[0:self.rows_limit]


class MyRequestsHomePagePart(HomePagePartBase):
    show_to_groups = (Groups.USERS, )
    template = "home_page/generic_request_list_page.html"
    code = 'my_requests'
    label = _(u"Мои заявки")
    no_rows = _(u"Нет созданных вами заявок")

    @property
    def data(self):
        return Request.objects.get_accessible_requests(self.request.user) \
                   .filter(status__code__in=(RequestStatus.PROJECT, RequestStatus.NEGOTIATION)) \
                   .order_by('created')[0:self.rows_limit]


class AwaitingPaymentHomePagePart(HomePagePartBase):
    show_to_groups = (Groups.ACCOUNTANTS, )
    template = "home_page/generic_request_list_page.html"
    code = 'awaiting_payment'
    label = _(u"Ожидают оплаты")
    no_rows = _(u"Нет заявок, ожидающих оплаты")

    @property
    def data(self):
        return Request.objects.filter(status__code=RequestStatus.NEGOTIATED_NO_PAYMENT) \
                   .order_by('accepted')[0:self.rows_limit]


class HomePage(TemplateView):
    _parts = (MyApprovalsHomePagePart, MyRequestsHomePagePart, AwaitingPaymentHomePagePart)

    def _get_parts(self, request):
        groups = [group.name for group in request.user.groups.all()]
        result = []
        for part_class in self._parts:
            part = part_class(request)
            if part.should_show(request.user, groups):
                result.append(part)
        return result

    def get(self, request, *args, **kwargs):
        return render(request, "home_page/index.html", {'parts': self._get_parts(request)})

