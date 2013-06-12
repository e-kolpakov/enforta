from django.contrib.auth import authenticate
from django.contrib.auth.views import login as default_login
from django.shortcuts import render
from DocApproval.models import UserProfile


def login(request, *args, **kwargs):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            try:
                profile = user.profile
            except UserProfile.DoesNotExist:
                return render(request, "authentication/profile_not_set.html")
    return default_login(request, *args, **kwargs)
