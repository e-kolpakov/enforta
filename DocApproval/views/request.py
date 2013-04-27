#-*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.shortcuts import (render, HttpResponseRedirect)
from django.views.generic import (TemplateView, UpdateView, CreateView)
from django.contrib import messages

from ..models import (Request, RequestStatus, UserProfile)
from ..forms import (CreateRequestForm, )
from ..url_naming.names import Request as RequestUrl
from ..messages import RequestMessages

from ..extensions.utility import get_url_base
from ..extensions.datatables import JsonConfigurableDatatablesBaseView


class CreateRequestView(CreateView):
    form_class = CreateRequestForm
    template_name = 'request/create.html'
    # TODO: add initialization of defaults, e.g. city, approver, etc.
    initial = {}

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_request = form.save(commit=False)
            new_request.status = RequestStatus.objects.get(pk=RequestStatus.PROJECT)
            new_request.creator = UserProfile.objects.get(user__exact=request.user)
            new_request.save()
            return HttpResponseRedirect(reverse(RequestUrl.DETAILS, kwargs={'pk': new_request.pk}))

        return render(request, self.template_name, {'form': form})


class ListRequestView(TemplateView):
    template_name = 'request/list.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'datatables_data': RequestUrl.LIST_JSON,
            'datatables_config': RequestUrl.LIST_JSON_CONF
        }
        )


class UpdateRequestView(UpdateView):
    template_name = 'request/update.html'
    model = Request


class DetailRequestView(TemplateView):
    template_name = 'request/details.html'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        exclude_fields = ['id', 'document']
        try:
            req = Request.objects.get(pk=pk)
            if not req.accepted:
                exclude_fields.append('accepted')
        except Request.DoesNotExist:
            req = None
            messages.error(request, RequestMessages.DOES_NOT_EXIST)

        return render(request, self.template_name, {
            'doc_request': req,
            'exclude_fields': exclude_fields
        })


class RequestListJson(JsonConfigurableDatatablesBaseView):
    model = Request
    link_field = 'name'
    display_fields = ('name', 'city', 'status', 'creator', 'send_on_approval', 'created', 'accepted')

    def get_links_config(self):
        return {'name': {'base_url': get_url_base(reverse(RequestUrl.DETAILS, kwargs={'pk': 0}))}}

    def get_initial_queryset(self):
        return self.model.objects.all()

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
            'accepted': accepted
        }


def archive(request, year=None, month=None):
    return render(request, "request/archive.html", {'year': year, 'month': month})