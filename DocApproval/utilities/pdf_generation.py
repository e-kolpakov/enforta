#-*- coding: utf-8 -*-
import StringIO
import os

from django.utils import html
from django.conf import settings
from django.http.response import HttpResponse
from django.template.context import RequestContext
from django.template.loader import render_to_string
from django.views.generic import View

from sx.pisa3 import pisa


class PdfView(View):
    pdf_template = None

    _resource_replacements = (
        (settings.MEDIA_URL, settings.MEDIA_ROOT),
        (settings.STATIC_URL, settings.STATIC_ROOT),
        ('../fonts/', settings.STATIC_ROOT + '/fonts/') # must be after STATIC_URL replacement
    )

    def _get_html(self, payload, context=None):
        payload.update({'media': self._media})
        return render_to_string(self.pdf_template, payload, context_instance=context)

    def _get_pdf(self, markup):
        pdf_file = StringIO.StringIO()
        pdf = pisa.pisaDocument(markup.encode("UTF-8"), pdf_file,
                                link_callback=self._fetch_resources)
        return not pdf.err, pdf_file.getvalue()

    def _get_payload(self, *args, **kwargs):
        raise NotImplementedError("Must be overridden in children")

    def _fetch_resources(self, uri, rel):
        for old_val, new_val in self._resource_replacements:
            if old_val in uri:
                uri = os.path.join(new_val, uri.replace(old_val, ""))
        return uri

    def get(self, request, *args, **kwargs):
        as_html = kwargs.get('as_html', False)
        self._media = 'screen' if as_html else 'print'
        markup = self._get_html(self._get_payload(*args, **kwargs), RequestContext(request))
        if as_html:
            return HttpResponse(markup)
        else:
            pdf_success, pdf_file = self._get_pdf(markup)
            if pdf_success:
                response = HttpResponse(pdf_file, mimetype='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=list.pdf'

            else:
                response = HttpResponse("Error generating PDF" + html.escape(markup))
            return response