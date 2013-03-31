from django.shortcuts import (render,)


def archive(request, year = None, month=None):
    return render(request, "request/archive.html", {'year':year, 'month':month})