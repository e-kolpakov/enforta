#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import (render, HttpResponseRedirect)
from django.views.generic import (TemplateView, UpdateView, CreateView)
from django.contrib import messages

from ..models import (Request, RequestStatus, UserProfile)
from ..forms import (CreateRequestForm,)
from ..url_naming.names import Request as RequestUrl
from ..messages import RequestMessages
from ..grids import RequestGrid


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
        return render(request, self.template_name, {'grid_config': RequestUrl.LIST_JSON_CONF})


class UpdateRequestView(UpdateView):
    template_name = 'request/update.html'
    model = Request


class DetailRequestView(TemplateView):
    template_name = 'request/details.html'

    def get(self, request, pk=None):
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


class RequestListJson(TemplateView):
    def get(self, request, *args, **kwargs):
        grid = RequestGrid()
        return HttpResponse(grid.get_json(request), mimetype="application/json")


def get_list_conf(request):
    grid = RequestGrid()
    return HttpResponse(grid.get_config(), mimetype="application/json")


def archive(request, year=None, month=None):
    return render(request, "request/archive.html", {'year':year, 'month':month})