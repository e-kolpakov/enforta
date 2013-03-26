from django.shortcuts import (render, HttpResponseRedirect)
from django.views.generic.edit import FormView

from DocApproval.extensions.authentication_helper import public_view
from ..forms import (PositionForm, ContactForm)


def index(request):
    return render(request, "index.html")


@public_view
def quicktest(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = ContactForm() # An unbound form

    return render(request, 'quicktest.html', {
        'form': form,
    })


class PositionEditView(FormView):
    form_class = PositionForm
    template_name = 'quicktest.html'
    success_url = '/thanks/'

    def form_valid(self, form):
        return super(PositionEditView, self).form_valid(form)
