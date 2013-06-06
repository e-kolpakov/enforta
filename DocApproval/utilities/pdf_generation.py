#-*- coding: utf-8 -*-
import StringIO
import logging

from django.utils import html
from django.conf import settings
from django.http.response import HttpResponse
from django.template.context import RequestContext
from django.template.loader import render_to_string
from django.views.generic import View

from weasyprint import HTML, CSS


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

    def _get_pdf(self, markup, base_url):
        logger = logging.getLogger(__name__)

        pdf_file = StringIO.StringIO()
        logger.critical("Creating weasy")
        weasy = HTML(
            file_obj=StringIO.StringIO(markup.encode("UTF-8")),
            encoding='UTF-8',
            base_url=base_url
        )
        logger.critical("Starting pdf generation")
        document = weasy.render(
            stylesheets=[CSS(file_obj=open("/home/john/GitRoot/Enforta/enforta/DocApproval/static/css/print.css"))])
        logger.critical("PDF generated, writing results")
        document.write_pdf(pdf_file)
        logger.critical("Results stored, returning")
        return pdf_file.getvalue()

    def _get_payload(self, *args, **kwargs):
        raise NotImplementedError("Must be overridden in children")

    def get(self, request, *args, **kwargs):
        as_html = kwargs.get('as_html', False)
        self._media = 'screen' if as_html else 'print'
        markup = self._get_html(self._get_payload(*args, **kwargs), RequestContext(request))
        if as_html:
            return HttpResponse(markup)
        else:
            try:
                pdf_file = self._get_pdf(markup, request.build_absolute_uri('/'))
                response = HttpResponse(pdf_file, mimetype='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=list.pdf'
            except Exception as e:
                response = HttpResponse(u"Error generating PDF: {0}<br/><br/>{1}".format(e, html.escape(markup)))
            return response