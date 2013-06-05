from django.views.generic.detail import SingleObjectMixin
from DocApproval.models.request import Request
from DocApproval.utilities.pdf_generation import PdfView


class ApprovalListPrint(PdfView, SingleObjectMixin):
    model = Request
    pdf_template = "request/request_approval_sheet.html"

    def _get_payload(self, *args, **kwargs):
        request = self.get_object()
        return {'request_name': request.name}