#-*- coding: utf-8 -*-
from django.utils.translation import ugettext as _


class CommonMessages:
    CREATE = _(u"Создать")
    MODIFY = _(u"Изменить")

    ACCESS_DENIED = _(u"Доступ запрещен")
    FILE_MISSING = _(u"[Файл не найден]")
    IMAGE_MISSING = _(u"[Изображение отсутсвует]")
    FORM_VALIDATION_ERROR = _(u"Введены некорректные данные")

    @classmethod
    def access_denied_message(cls, detailed_message):
        return u"{0}: {1}".format(cls.ACCESS_DENIED, detailed_message)


class RequestMessages:
    CREATE_REQUEST = _(u"Новая заявка")
    MODIFY_REQUEST = _(u"Изменение заявки")
    REQUEST_CREATED = _(u"Заявка создана успешно")
    REQUEST_MODIFIED = _(u"Заявка изменена успешно")

    DOES_NOT_EXIST = _(u"Запрошенной заявки не существует")
    ACCESS_DENIED = _(u"Доступ запрещен")
    CANT_CHANGE_CITY = _(u"Невозможно изменить город существующей заявки")

    CURRENT_REVIEVERS = _(u"Ожидает утверждения")


class ProfileMessages:
    DOES_NOT_EXIST = _(u"Запрошен профиль неизвестного пользователя")


class ContractMessages:
    NOT_PAYED = _(u"Не оплачен")


class ApprovalRouteMessages:
    NEW_APPROVAL_ROUTE = _(u"Новый маршрут утверждения")
    NEW_TEMPLATE_APPROVAL_ROUTE = _(u"Новый шаблонный маршрут утверждения")

    STEPS_COUNT = _(u"Количество этапов")

    DEFAULT_TEMPLATE_APPROVAL_ROUTE_NAME = _(u"Шаблонный маршрут №{0}")


class PeriodMessages:
    DAYS = _(u"дней")