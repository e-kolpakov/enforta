#-*- coding: utf-8 -*-
from django.utils.translation import ugettext as _


class CommonMessages:
    ACCESS_DENIED = _(u"Доступ запрещен")
    FILE_MISSING = _(u"[Файл не найден]")
    IMAGE_MISSING = _(u"[Изображение отсутсвует]")
    FORM_VALIDATION_ERROR = _(u"Введены некорректные данные")

    @classmethod
    def access_denied_message(cls, detailed_message):
        return u"{0}: {1}".format(cls.ACCESS_DENIED, detailed_message)


class RequestMessages:
    REQUEST_CREATED = _(u"Заявка создана успешно")
    REQUEST_MODIFIED = _(u"Заявка изменена успешно")
    DOES_NOT_EXIST = _(u"Запрошенной заявки не существует")
    ACCESS_DENIED = _(u"Доступ запрещен")
    CANT_CHANGE_CITY = _(u"Невозможно изменить город существующей заявки")


class ProfileMessages:
    DOES_NOT_EXIST = _(u"Запрошен профиль неизвестного пользователя")


class ContractMessages:
    NOT_PAYED = _(u"Не оплачен")


class ApprovalRouteMessages:
    NEW_APPROVAL_ROUTE = _(u"Новый маршрут утверждения")
    NEW_TEMPLATE_APPROVAL_ROUTE = _(u"Новый шаблонный маршрут утверждения")