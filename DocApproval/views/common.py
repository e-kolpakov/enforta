from django.shortcuts import (render, HttpResponseRedirect)
from django.views.generic.edit import FormView

from DocApproval.extensions.authentication_helper import public_view
from ..forms import *


def index(request):
    return render(request, "index.html")


@public_view
def quicktest(request):
    return render(request, "quicktest.html")


class RequestEditView(FormView):
    form_class = CreateRequestForm
    template_name = 'request_edit.html'
    success_url = '/quicktest/'

    def post(self, request, *args, **kwargs):
        form = CreateRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})

    def get(self, request, *args, **kwargs):
        form = CreateRequestForm()
        return render(request, self.template_name, {'form': form})
