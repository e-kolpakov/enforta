#-*- coding: utf-8 -*-
from django.utils.translation import ugettext as _


class Common:
    ACCESS_DENIED = _(u"Доступ запрещен")
    FILE_MISSING = _(u"[Файл не найден]")
    IMAGE_MISSING = _(u"[Изображение отсутсвует]")

    @classmethod
    def access_denied_message(cls, detailed_message):
        return u"{0}: {1}".format(cls.ACCESS_DENIED, detailed_message)


class RequestMessages:
    REQUEST_CREATED = _(u"Заявка создана успешно")
    DOES_NOT_EXIST = _(u"Запрошенной заявки не существует")
    REQUEST_CREATION_ERROR = _(u"Произошла ошибка сохранения")


class ProfileMessages:
    DOES_NOT_EXIST = _(u"Запрошен профиль неизвестного пользователя")
