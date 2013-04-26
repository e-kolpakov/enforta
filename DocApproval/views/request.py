#-*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.shortcuts import (render, HttpResponseRedirect)
from django.views.generic import (TemplateView, UpdateView, CreateView)
from django.contrib import messages

from django_datatables_view.base_datatable_view import BaseDatatableView

from ..models import (Request, RequestStatus, UserProfile)
from ..forms import (CreateRequestForm, )
from ..url_naming.names import Request as RequestUrl
from ..messages import RequestMessages


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
        return render(request, self.template_name, {'ajax_backend_url': RequestUrl.LIST_JSON})


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


class RequestListJson(BaseDatatableView):
    order_columns = ['name', 'city', 'status', 'creator', 'send_on_approval', 'created', 'accepted']

    def get_initial_queryset(self):
        # return queryset used as base for futher sorting/filtering
        # these are simply objects displayed in datatable
        return Request.objects.all()

    def filter_queryset(self, qs):
        # use request parameters to filter queryset

        # simple example:
        sSearch = self.request.POST.get('sSearch', None)
        if sSearch:
            qs = qs.filter(name__istartswith=sSearch)

        return qs

    def prepare_results(self, qs):
        # prepare list with output column data
        # queryset is already paginated here
        json_data = []
        for item in qs:
            accepted = item.accepted.strftime("%Y-%m-%d") if item.accepted is not None else "---"
            json_data.append([
                item.name,
                item.city.city_name,
                item.status.status_name,
                item.creator.get_full_name(),
                item.send_on_approval.get_full_name(),
                item.created.strftime("%Y-%m-%d"),
                accepted
            ])
        return json_data


def archive(request, year=None, month=None):
    return render(request, "request/archive.html", {'year': year, 'month': month})