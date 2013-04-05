from django.core.urlresolvers import reverse
from django.shortcuts import (render, HttpResponseRedirect)
from django.views.generic import TemplateView

from ..models import (RequestStatus, UserProfile)
from ..forms import (CreateRequestForm,)
from ..url_naming.names import (Request)


class CreateRequestView(TemplateView):
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
            HttpResponseRedirect(reverse(Request.DETAILS))

        return render(request, self.template_name, {'form': form})



def archive(request, year = None, month=None):
    return render(request, "request/archive.html", {'year':year, 'month':month})