# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

def index(request):
    return render_to_response("index.html")

@login_required()
def quicktest(request):
    return render_to_response('quicktest.html', {'auth': request.user.is_authenticated(), 'user': request.user})


def login(request):
    return render_to_response('login.html')