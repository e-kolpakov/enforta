# -*- coding: utf-8 -*-
import logging
import itertools
from datetime import date

from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.template.defaultfilters import date as _date
from django.views.generic.detail import SingleObjectMixin
from django.utils.translation import ugettext as _

from DocApproval.models import Request, UserProfile, Department
from DocApproval.utilities.pdf_generation import PdfView


class ApprovalListPrint(PdfView, SingleObjectMixin):
    model = Request
    pdf_template = "request/request_approval_sheet.html"

    def _get_payload(self, *args, **kwargs):
        req = self.get_object()
        generator = ApprovalListGenerator(req)
        return {
            'request': req,
            'rows': generator.get_rows(),
            'date_format': generator.date_format
        }


class ApprovalListGenerator(object):
    _logger = logging.getLogger(__name__ + ".ApprovalListPrint")
    date_format = "«d» E Yг."

    # show year in 201_ format - with blank trailing digit
    date_tpl = u'«___»__________{0}_г.'.format(date.today().year / 10)
    signature = u"подпись"

    request_comment_tpl = u"<div class='comment'>{0}<div>"
    approved_by_tpl = u"<div class='approved-by'>{0}</div><div class='comment'>{1}</div>"

    def __init__(self, request):
        self._request = request
        self._approval_actions = list(request.successful_approval.get_approval_actions())
        self._approvers = [action.step.approver for action in self._approval_actions]

    @property
    def request(self):
        return self._request

    @property
    def approval_actions(self):
        return self._approval_actions

    @property
    def approvers(self):
        return self._approvers

    def get_rows(self):
        return self._get_rows()

    def _get_departments(self, city):
        return Department.objects.get_departments_for_list(city)

    def _make_signature_img(self, image):
        img_url = image.url if image else ''
        return mark_safe("<img src='{0}' class='signature'/>".format(img_url))

    def _format_date(self, date):
        return _date(date, self.date_format)

    def _get_manager_approval(self):
        signature, action_date = None, None
        try:
            manager = self.request.creator.manager
        except UserProfile.DoesNotExist:
            self._logger.warning("Manager is not set for user {0}".format(self.request.creator.pk))
            return signature, action_date

        action = self.request.successful_approval.get_approval_action(manager)
        if action:
            signature = manager.sign
            action_date = action.action_taken
        else:
            self._logger.warning(
                "Manager have not taken action in approval process of request {0}".format(self.request.pk))

        return signature, action_date

    def _get_general_info_rows(self):
        return (
            ApprovalListRow.get_row(ApprovalListRow.SIX_CELLS_ROW),
            ApprovalListRow.get_row(
                ApprovalListRow.SIX_CELLS_ROW, cell_contents={1: u"Документ", 3: self.request.name}
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
                    6: self._format_date(self.request.created)}
            ),
            ApprovalListRow.get_row(ApprovalListRow.SIX_CELLS_ROW),
            ApprovalListRow.get_row(
                ApprovalListRow.SIX_CELLS_ROW,
                cell_contents={1: u"Инициатор заказа", 3: self.request.creator.full_name, 4: u"Дирекция"}),
            ApprovalListRow.get_row(ApprovalListRow.SIX_CELLS_ROW, cell_contents={3: u"(Ф.И.О.)"}),
            ApprovalListRow.get_row(ApprovalListRow.SIX_CELLS_ROW, cell_contents={1: u"Контрагент"}),
            ApprovalListRow.get_row(ApprovalListRow.SIX_CELLS_ROW),
            ApprovalListRow.get_row(ApprovalListRow.SIX_CELLS_ROW, cell_contents={1: u"Предмет договора"}),
            ApprovalListRow.get_row(ApprovalListRow.SIX_CELLS_ROW),
            ApprovalListRow.get_row(ApprovalListRow.SIX_CELLS_ROW),
            ApprovalListRow.get_row(ApprovalListRow.SIX_CELLS_ROW,
                                    cell_contents={1: u"Сумма", 3: "{0:.2f}".format(self.request.contract.cost),
                                                   4: u"Валюта", 6: self.request.contract.currency.caption_plural}),
            ApprovalListRow.get_row(ApprovalListRow.SIX_CELLS_ROW),
            ApprovalListRow.get_row(ApprovalListRow.ONE_CELL_ROW, css_class="comment-label",
                                    cell_contents={1: u"Комментарий"}),
            ApprovalListRow.get_row(ApprovalListRow.ONE_CELL_ROW, height=2, css_class="comment-text",
                                    cell_contents={
                                        1: mark_safe(self.request_comment_tpl.format(escape(self.request.comments)))
                                    })
        )

    def _get_creator_and_manager_rows(self):
        creator_signature, creator_action_date = self.request.creator.sign, self.request.created
        manager_signature, manager_action_date = self._get_manager_approval()

        creator_sign_img = self._make_signature_img(creator_signature)
        manager_sign_img = self._make_signature_img(manager_signature) if manager_signature else ''
        date_tpl = self.date_tpl
        return (
            ApprovalListRow.get_row(
                ApprovalListRow.FOUR_CELL_ROW,
                height=2,
                cell_contents={
                    1: creator_sign_img,
                    2: self._format_date(creator_action_date) if creator_action_date else date_tpl,
                    3: manager_sign_img,
                    4: self._format_date(manager_action_date) if manager_action_date else date_tpl,
                }),
            ApprovalListRow.get_row(ApprovalListRow.FOUR_CELL_ROW,
                                    cell_contents={1: u"Подпись инициатора", 3: u"Подпись руководителя дирекции"})
        )

    def _get_approved_part(self, actor, approver, comment):
        approved_by = _(u"Согласовано: {0}").format(actor.full_name)
        if actor != approver:
            approved_by += _(u" от имени {0}").format(approver.full_name_accusative)

        result = mark_safe(self.approved_by_tpl.format(escape(approved_by), comment))
        return result

    def _get_approver_rows(self, approval):
        approver = approval.step.approver
        actor = approval.actor
        return (
            ApprovalListRow.get_row(
                ApprovalListRow.THREE_CELL_ROW1,
                height=2,
                cell_contents={
                    1: self._get_approved_part(actor, approver, approval.comment),
                    2: self._make_signature_img(actor.sign),
                    3: self._format_date(approval.action_taken)
                }
            ),
            ApprovalListRow.get_row(ApprovalListRow.THREE_CELL_ROW2,
                                    cell_contents={1: u"Фамилия И.О. ", 2: self.signature}),
        )

    def _get_department_rows(self, department):
        rslt = [
            ApprovalListRow.get_row(ApprovalListRow.THREE_CELL_ROW3,
                                    cell_contents={1: department.name, 2: u"Дата поступления на согласование",
                                                   3: self.date_tpl}),
            ApprovalListRow.get_row(ApprovalListRow.THREE_CELL_ROW1, cell_contents={1: u"Замечания"}),
            ApprovalListRow.get_row(ApprovalListRow.THREE_CELL_ROW1),
            ApprovalListRow.get_row(ApprovalListRow.THREE_CELL_ROW1)
        ]

        approval = [approval for approval in self.approval_actions if
                    approval.step.approver == department.responsible_user]
        eff_approval = approval[0] if approval else None
        if eff_approval:
            approved_by_rows = self._get_approver_rows(eff_approval)
        else:
            approved_by_rows = [
                ApprovalListRow.get_row(ApprovalListRow.THREE_CELL_ROW1,
                                        cell_contents={1: u"Согласовано", 3: self.date_tpl}),
                ApprovalListRow.get_row(ApprovalListRow.THREE_CELL_ROW2, cell_contents={2: self.signature})
            ]
        rslt.extend(approved_by_rows)
        return rslt

    def _get_rows(self):
        departments = self._get_departments(self.request.city)
        department_signers = [department.responsible_user for department in departments if department.responsible_user]

        general_info_rows = self._get_general_info_rows()
        creator_and_manager_rows = self._get_creator_and_manager_rows()
        dep_rows = itertools.chain.from_iterable(
            self._get_department_rows(dep) for dep in self._get_departments(self.request.city)
        )

        approval_rows = itertools.chain.from_iterable(
            [
                self._get_approver_rows(action)
                for action in self.approval_actions
                if action.step.approver not in department_signers
            ]
        )

        return itertools.chain(general_info_rows, creator_and_manager_rows, approval_rows, dep_rows)


class ApprovalListRow(object):
    SIX_CELLS_ROW = 'six-cell'
    FOUR_CELL_ROW = 'four-cell'
    THREE_CELL_ROW1 = 'three-cell-row1'
    THREE_CELL_ROW2 = 'three-cell-row2'
    THREE_CELL_ROW3 = 'three-cell-row3'
    ONE_CELL_ROW = 'one-cell'

    _cell_definitions = {
        SIX_CELLS_ROW: {
            'number': 6,
            'colspans': [1 for i in range(6)],
            'classes': tuple('cell{0}'.format(i) for i in range(1, 7))
        },
        FOUR_CELL_ROW: {
            'number': 4,
            'colspans': [2, 1, 2, 1],
            'classes': ('cell1-colspan2 center', 'cell3', 'cell4-colspan2', 'cell6',),
        },
        THREE_CELL_ROW1: {
            'number': 3,
            'colspans': [3, 2, 1],
            'classes': ('cell1-colspan3', 'cell4-colspan2', 'cell6',),
        },
        THREE_CELL_ROW2: {
            'number': 3,
            'colspans': [3, 2, 1],
            'classes': ('cell1-colspan3 center', 'cell4-colspan2', 'cell6',),
        },
        THREE_CELL_ROW3: {
            'number': 3,
            'colspans': [3, 2, 1],
            'classes': ('cell1-colspan3 department', 'cell4-colspan2', 'cell6',),
        },
        ONE_CELL_ROW: {
            'number': 1,
            'colspans': [6],
            'classes': ('cell-colspan6',)
        },
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
    def get_row(cls, row_type, cell_contents=None, height=1, css_class=None):
        """ Generates row by template
            @param row_type - type of the row (see ApprovalListRow constants)
            @param cell_contents - dictionary in format column_number (1-based): column_contents
            @param height - row height class (idx only: 1, 2, 3)
        """
        contents = cell_contents if cell_contents else {}
        cell_def = cls._cell_definitions[row_type]
        columns = [
            {'content': contents.get(i + 1, ''), 'colspan': cell_def['colspans'][i]}
            for i in range(0, cell_def['number'])
        ]
        return cls(columns=columns, column_classes=cell_def['classes'], css_class=css_class, height=height)


class ApprovalListCell(object):
    def __init__(self, **kwargs):
        cnt = kwargs.get('content', None)
        self.content = cnt if cnt else mark_safe('&nbsp;')
        self.css_class = kwargs.get('css_class', '')
        self.colspan = kwargs.get('colspan', 1)



