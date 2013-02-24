#-*- coding: utf-8 -*-
class RequestStatus:
    PROJECT = 1
    NEGOTIATION = 2
    NEGOTIATED_NO_PAYMENT = 3
    ACTIVE = 4
    OUTDATED = 5
    BILL_REQUIRED = 6

    _status_names = {
        PROJECT: "Проект",
        NEGOTIATION: "В согласовании",
        NEGOTIATED_NO_PAYMENT: "Согласован, но не оплачен",
        ACTIVE: "В работе",
        OUTDATED: "Истек срок действия",
        BILL_REQUIRED: "Требуется счет"
    }

    @classmethod
    def get_readable_name(cls, status):
        return cls._status_names[status]