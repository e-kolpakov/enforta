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
    ONLY_PROJECT_REQUESTS_EDITABLE = _(u'Заявки могут быть отредактированы только в статусе "Проект"')

    CURRENT_REVIEVERS = _(u"Ожидает утверждения")

    ACTION_IS_NOT_ACCESSIBLE = _(u"Нельзя совершить выбранное действие над данной заявкой")


class ProfileMessages:
    DOES_NOT_EXIST = _(u"Запрошен профиль неизвестного пользователя")
    SIGNATURE_EMPTY = _(u"Не задана ваша подпись. Листы утверждения с вашим участием будут созданы без вашей подписи.")


class ContractMessages:
    NOT_PAYED = _(u"Не оплачен")


class ApprovalRouteMessages:
    NEW_APPROVAL_ROUTE = _(u"Новый маршрут утверждения")
    NEW_TEMPLATE_APPROVAL_ROUTE = _(u"Новый шаблонный маршрут утверждения")

    STEPS_COUNT = _(u"Количество этапов")
    DEFAULT_TEMPLATE_APPROVAL_ROUTE_NAME = _(u"Шаблонный маршрут №{0}")

    GENERIC_ROUTE_ERROR_MESSAGE = _(u"Ошибка сохранения маршрута: ")
    NON_EDITABLE_ROUTE_MESSAGE = _(
        u"Редактирование маршрута утверждения возможно только для заявок, находящихся в статусе проекта")

    EMPTY_ROUTE_STEPS = _(u"Не заданы этапы утверждения")
    ROUTE_TEMPLATE_SWITCH_NOT_ALLOWED = _(u"Изменение маршрута запрещено")
    NON_AVAILABLE_FOR_TEMPLATE = _(u"{0} не имеет смысла для шаблонного маршрута")


class PeriodMessages:
    DAYS = _(u"дней")