# -*- coding: utf-8 -*-
import logging
import itertools

from django.utils.safestring import mark_safe
from django.template.defaultfilters import date as _date
from django.views.generic.detail import SingleObjectMixin

from DocApproval.models.request import Request
from DocApproval.models.user import UserProfile
from DocApproval.utilities.pdf_generation import PdfView


class ApprovalListCell(object):
    def __init__(self, **kwargs):
        cnt = kwargs.get('content', None)
        self.content = cnt if cnt else mark_safe('&nbsp;')
        self.css_class = kwargs.get('css_class', '')
        self.colspan = kwargs.get('colspan', 1)


class ApprovalListRow(object):
    SIX_CELLS_ROW = 'six-cell'
    FOUR_CELL_ROW = 'four-cell'
    THREE_CELL_ROW1 = 'three-cell-row1'
    THREE_CELL_ROW2 = 'three-cell-row2'
    THREE_CELL_ROW3 = 'three-cell-row3'

    _cell_definitions = {
        SIX_CELLS_ROW: {
            'number': 6,
            'colspans': [1 for i in range(6)],
            'classes': tuple('cell{0}'.format(i) for i in range(1, 7))
        },
        FOUR_CELL_ROW: {
            'number': 4,
            'colspans': [2, 1, 2, 1],
            'classes': tuple(('cell1-colspan2 center', 'cell3', 'cell4-colspan2', 'cell6')),
        },
        THREE_CELL_ROW1: {
            'number': 3,
            'colspans': [3, 2, 1],
            'classes': tuple(('cell1-colspan3', 'cell4-colspan2', 'cell6')),
        },
        THREE_CELL_ROW2: {
            'number': 3,
            'colspans': [3, 2, 1],
            'classes': tuple(('cell1-colspan3 center', 'cell4-colspan2', 'cell6')),
        },
        THREE_CELL_ROW3: {
            'number': 3,
            'colspans': [3, 2, 1],
            'classes': tuple(('cell1-colspan3 department', 'cell4-colspan2', 'cell6')),
        }
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
    def get_row(cls, row_type, cell_contents=None, height=1):
        """ Generates row with six cells.
            @param cell_contents - dictionary in format column_number (1-based): column_contents
        """
        contents = cell_contents if cell_contents else {}
        cell_def = cls._cell_definitions[row_type]
        columns = [
            {'content': contents.get(i + 1, ''), 'colspan': cell_def['colspans'][i]}
            for i in range(0, cell_def['number'])
        ]
        return cls(columns=columns, column_classes=cell_def['classes'], height=height)


class ApprovalListPrint(PdfView, SingleObjectMixin):
    model = Request
    pdf_template = "request/request_approval_sheet.html"
    _logger = logging.getLogger(__name__ + ".ApprovalListPrint")

    date_format = "«d» E Yг."

    date_tpl = u'«___»__________201_г.'
    signature = u"подпись"

    departments = (
        u"Бухгалтерия",
        u"Финансовый отдел",
        u"Дирекция по экономической безопасности",
        u"Юридический отдел",
    )

    # Self-encapsulation: one day departments will live in the database, so this method will fetch them there
    def _get_departments(self):
        return self.departments

    def _make_signature_img(self, url):
        return mark_safe("<img src='{0}' class='signature'/>".format(url))

    def _format_date(self, date):
        return _date(date, self.date_format)

    def _get_manager_approval(self, request):
        signature, action_date = None, None
        try:
            manager = request.creator.manager
        except UserProfile.DoesNotExist:
            self._logger.warning("Manager is not set for user {0}".format(request.creator.pk))
            return signature, action_date

        action = request.successful_approval.get_approval_action(manager)
        if action:
            signature = manager.sign.url
            action_date = action.action_taken
        else:
            self._logger.warning("Manager have not taken action in approval process of request {0}".format(request.pk))

        return signature, action_date

    def _get_general_info_rows(self, request):
        return (
            ApprovalListRow.get_row(ApprovalListRow.SIX_CELLS_ROW),
            ApprovalListRow.get_row(
                ApprovalListRow.SIX_CELLS_ROW, cell_contents={1: u"Документ", 3: request.name}
            ),
            ApprovalListRow.get_row(
                ApprovalListRow.SIX_CELLS_ROW,
                cell_contents={3: u"(основной договор, доп. соглашение)"}
            ),
            ApprovalListRow.get_row(ApprovalListRow.SIX_CELLS_ROW),
            ApprovalListRow.get_row(
                ApprovalListRow.SIX_CELLS_ROW,
                cell_contents={
                    1: u"Закупочный заказ",
                    4: u"Дата",
                    6: self._format_date(request.created)}
            ),
            ApprovalListRow.get_row(ApprovalListRow.SIX_CELLS_ROW),
            ApprovalListRow.get_row(
                ApprovalListRow.SIX_CELLS_ROW,
                cell_contents={1: u"Инициатор заказа", 3: request.creator.full_name, 4: u"Дирекция"}),
            ApprovalListRow.get_row(ApprovalListRow.SIX_CELLS_ROW, cell_contents={3: u"(Ф.И.О.)"}),
            ApprovalListRow.get_row(ApprovalListRow.SIX_CELLS_ROW, cell_contents={1: u"Контрагент"}),
            ApprovalListRow.get_row(ApprovalListRow.SIX_CELLS_ROW),
            ApprovalListRow.get_row(ApprovalListRow.SIX_CELLS_ROW, cell_contents={1: u"Предмет договора"}),
            ApprovalListRow.get_row(ApprovalListRow.SIX_CELLS_ROW),
            ApprovalListRow.get_row(ApprovalListRow.SIX_CELLS_ROW),
            ApprovalListRow.get_row(ApprovalListRow.SIX_CELLS_ROW, cell_contents={1: u"Сумма", 4: u"Валюта"}),
            ApprovalListRow.get_row(ApprovalListRow.SIX_CELLS_ROW),
            ApprovalListRow.get_row(ApprovalListRow.SIX_CELLS_ROW, cell_contents={1: u"Комментарии"}),
            ApprovalListRow.get_row(ApprovalListRow.SIX_CELLS_ROW),
            ApprovalListRow.get_row(ApprovalListRow.SIX_CELLS_ROW),
        )

    def _get_creator_and_manager_rows(self, request):
        creator_signature, creator_action_date = request.creator.sign.url, request.created
        manager_signature, manager_action_date = self._get_manager_approval(request)

        creator_sign_img = self._make_signature_img(creator_signature)
        manager_sign_img = self._make_signature_img(manager_signature) if manager_signature else ''
        date_tpl = self.date_tpl
        return (
            ApprovalListRow.get_row(
                ApprovalListRow.FOUR_CELL_ROW,
                cell_contents={
                    1: creator_sign_img,
                    2: self._format_date(creator_action_date) if creator_action_date else date_tpl,
                    3: manager_sign_img,
                    4: self._format_date(manager_action_date) if manager_action_date else date_tpl,
                }),
            ApprovalListRow.get_row(ApprovalListRow.FOUR_CELL_ROW,
                                    cell_contents={1: u"Подпись инициатора", 3: u"Подпись руководителя дирекции"})
        )

    def _get_approver_rows(self, approval):
        user = approval.step.approver
        return (
            ApprovalListRow.get_row(
                ApprovalListRow.THREE_CELL_ROW1,
                cell_contents={
                    1: u"Согласовано: {0}".format(user.full_name),
                    2: self._make_signature_img(user.sign.url),
                    3: self._format_date(approval.action_taken)
                }
            ),
            ApprovalListRow.get_row(ApprovalListRow.THREE_CELL_ROW2,
                                    cell_contents={1: u"Фамилия И.О. ", 2: self.signature}),
        )

    def _get_department_rows(self, department):
        return (
            ApprovalListRow.get_row(ApprovalListRow.THREE_CELL_ROW3,
                                    cell_contents={1: department, 2: u"Дата поступления на согласование",
                                                   3: self.date_tpl}),
            ApprovalListRow.get_row(ApprovalListRow.THREE_CELL_ROW1, cell_contents={1: u"Замечания"}),
            ApprovalListRow.get_row(ApprovalListRow.THREE_CELL_ROW1),
            ApprovalListRow.get_row(ApprovalListRow.THREE_CELL_ROW1),
            ApprovalListRow.get_row(ApprovalListRow.THREE_CELL_ROW1,
                                    cell_contents={1: u"Согласовано", 3: self.date_tpl}),
            ApprovalListRow.get_row(ApprovalListRow.THREE_CELL_ROW2, cell_contents={2: self.signature}),
        )

    def _get_rows(self, request):
        general_info_rows = self._get_general_info_rows(request)
        creator_and_manager_rows = self._get_creator_and_manager_rows(request)
        dep_rows = itertools.chain.from_iterable(self._get_department_rows(dep) for dep in self._get_departments())

        approval_rows = itertools.chain.from_iterable(
            [self._get_approver_rows(action) for action in request.successful_approval.get_approval_actions()]
        )

        return itertools.chain(general_info_rows, creator_and_manager_rows, approval_rows, dep_rows)

    def _get_payload(self, *args, **kwargs):
        req = self.get_object()
        return {
            'request': req,
            'rows': self._get_rows(req),
            'date_format': self.date_format
        }