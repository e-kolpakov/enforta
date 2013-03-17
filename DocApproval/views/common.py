from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def quicktest(request):
    return render(request, 'quicktest.html')
