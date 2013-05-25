import os

from django.conf import settings
from django.http.response import Http404
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper


def media(request, filename):
    if "../" in filename:
        raise Http404()

    path = os.path.join(settings.MEDIA_ROOT, filename)
    wrapper = FileWrapper(file(path))
    response = HttpResponse(wrapper, content_type='application/octet-stream')
    response['Content-Length'] = os.path.getsize(path)
    return response