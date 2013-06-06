# -*- coding: utf-8 -*-
import itertools
from django.utils.safestring import mark_safe

from django.views.generic.detail import SingleObjectMixin
from DocApproval.models.request import Request
from DocApproval.utilities.pdf_generation import PdfView


class ApprovalListCell(object):
    def __init__(self, **kwargs):
        cnt = kwargs.get('content', None)
        self.content = cnt if cnt else mark_safe('&nbsp;')
        self.css_class = kwargs.get('css_class', '')
        self.colspan = kwargs.get('colspan', 1)


class ApprovalListRow(object):
    _cell_classes = {
        6: tuple('cell{0}'.format(i) for i in range(1, 7)),
        4: tuple(('cell1-colspan2', 'cell3', 'cell4-colspan2', 'cell6')),
        3: tuple(('cell1-colspan3', 'cell4-colspan2', 'cell6'))
    }

    _cell_colspans = {
        6: [1 for i in range(6)],
        4: [2, 1, 2, 1],
        3: [3, 2, 1]
    }

    def __init__(self, columns=None, column_classes=None, css_class=None, height=1):
        self.height = height
        clmns = columns if columns else tuple()
        self.cells = self._parse_columns(clmns, column_classes)
        eff_css_class = css_class if css_class else ''
        self.css_class = 'row-height{0} {1}'.format(height, eff_css_class)

    def _parse_columns(self, columns, column_classes):
        result = []
        for column, column_class in itertools.izip_longest(columns, column_classes):
            result.append(
                ApprovalListCell(css_class=column_class, content=column['content'], colspan=column['colspan']))
        return result

    @classmethod
    def get_row(cls, cells_number, cell_contents=None, height=1):
        """ Generates row with six cells.
            @param cell_contents - dictionary in format column_number (1-based): column_contents
        """
        contents = cell_contents if cell_contents else {}
        cell_classes = cls._cell_classes[cells_number]
        cell_colspans = cls._cell_colspans[cells_number]
        columns = [
            {'content': contents.get(i + 1, ''), 'colspan': cell_colspans[i]}
            for i in range(0, cells_number)
        ]
        return cls(columns=columns, column_classes=cell_classes, height=height)


class ApprovalListPrint(PdfView, SingleObjectMixin):
    model = Request
    pdf_template = "request/request_approval_sheet.html"

    def _get_date_tpl(self):
        return u'"___"_____________ 201_г.'

    def _get_rows(self, request):
        date_tpl = self._get_date_tpl()
        return (
            ApprovalListRow.get_row(6),
            ApprovalListRow.get_row(6, cell_contents={1: u"Документ"}),
            ApprovalListRow.get_row(6, cell_contents={3: u"(основной договор, доп. соглашение)"}),
            ApprovalListRow.get_row(6),
            ApprovalListRow.get_row(6, cell_contents={1: u"Закупочный заказ", 4: u"Дата"}),
            ApprovalListRow.get_row(6),
            ApprovalListRow.get_row(6, cell_contents={1: u"Инициатор заказа", 4: u"Дирекция"}),
            ApprovalListRow.get_row(6, cell_contents={3: u"(Ф.И.О.)"}),
            ApprovalListRow.get_row(6, cell_contents={1: u"Контрагент"}),
            ApprovalListRow.get_row(6),
            ApprovalListRow.get_row(6, cell_contents={1: u"Предмет договора"}),
            ApprovalListRow.get_row(6),
            ApprovalListRow.get_row(6),
            ApprovalListRow.get_row(6, cell_contents={1: u"Сумма", 4: u"Валюта"}),
            ApprovalListRow.get_row(6),
            ApprovalListRow.get_row(6, cell_contents={1: u"Комментарии"}),
            ApprovalListRow.get_row(6),
            ApprovalListRow.get_row(6),
            ApprovalListRow.get_row(4, height=2, cell_contents={2: date_tpl, 4: date_tpl}),
        )

    def _get_payload(self, *args, **kwargs):
        req = self.get_object()
        return {
            'request': req,
            'rows': self._get_rows(req)
        }