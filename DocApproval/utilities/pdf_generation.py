#-*- coding: utf-8 -*-
import os
import StringIO
import logging

from django.utils import html
from django.conf import settings
from django.http.response import HttpResponse
from django.template.context import RequestContext
from django.template.loader import render_to_string
from django.views.generic import View

from weasyprint import HTML


class PdfView(View):
    pdf_template = None

    _resource_replacements = (
        (settings.MEDIA_URL, settings.MEDIA_ROOT),
        (settings.STATIC_URL, settings.STATIC_ROOT)
    )

    def _get_html(self, payload, context=None):
        payload.update({'media': self._media})
        return render_to_string(self.pdf_template, payload, context_instance=context)

    def _get_pdf(self, markup):
        logger = logging.getLogger(__name__)
        base_url = self.base_url if self.base_url else ''
        pdf_file = StringIO.StringIO()
        logger.info("Creating weasy")
        weasy = HTML(
            file_obj=StringIO.StringIO(markup.encode("UTF-8")),
            encoding='UTF-8',
            base_url=base_url,
            url_fetcher=self._url_fetcher
        )
        logger.info("Starting pdf generation")
        weasy.write_pdf(pdf_file)
        logger.info("PDF generated, returning")
        return pdf_file.getvalue()

    def _url_fetcher(self, url):
        if self.base_url and self.base_url in url:
            url = url.replace(self.base_url, '/')
        for network_path, disk_path in self._resource_replacements:
            if network_path in url:
                url = os.path.join(disk_path, url.replace(network_path, ''))
                break
        return {'file_obj': open(url, 'r')}


    def _get_payload(self, *args, **kwargs):
        raise NotImplementedError("Must be overridden in children")

    def get(self, request, *args, **kwargs):
        try:
            as_html = kwargs.get('as_html', False)
            self._media = 'screen' if as_html else 'print'
            markup = self._get_html(self._get_payload(*args, **kwargs), RequestContext(request))
            if as_html:
                return HttpResponse(markup)
            else:
                try:
                    self.base_url = request.build_absolute_uri('/')
                    pdf_file = self._get_pdf(markup)
                    response = HttpResponse(pdf_file, mimetype='application/pdf')
                    response['Content-Disposition'] = 'attachment; filename=list.pdf'
                except Exception as e:
                    response = HttpResponse(u"Error generating PDF: {0}<br/><br/>{1}".format(e, html.escape(markup)))
                return response
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(e)
            raise