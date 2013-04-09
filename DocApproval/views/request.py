#-*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.shortcuts import (render, HttpResponseRedirect)
from django.views.generic import (TemplateView, ListView, UpdateView, CreateView)
from django.contrib import messages

from ..models import (Request, RequestStatus, UserProfile)
from ..forms import (CreateRequestForm,)
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
            HttpResponseRedirect(reverse(RequestUrl.DETAILS, kwargs={'pk': new_request.pk}))

        return render(request, self.template_name, {'form': form})


class ListRequestView(ListView):
    template_name = 'request/list.html'
    model = Request


class UpdateRequestView(UpdateView):
    template_name = 'request/update.html'
    model = Request


class DetailRequestView(TemplateView):
    template_name = 'request/details.html'

    def get(self, request, pk=None):
        try:
            req = Request.objects.get(pk=pk)
        except Request.DoesNotExist:
            req = None
            messages.error(request, RequestMessages.DOES_NOT_EXIST)

        return render(request, self.template_name, {'request': req})

def archive(request, year=None, month=None):
    return render(request, "request/archive.html", {'year':year, 'month':month})