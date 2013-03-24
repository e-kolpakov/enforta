from django.shortcuts import render
from DocApproval.extensions.authentication_helper import public_view


def index(request):
    return render(request, "index.html")


@public_view
def quicktest(request):
    return render(request, 'quicktest.html')
