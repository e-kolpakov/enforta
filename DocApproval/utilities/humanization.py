#-*- coding: utf-8 -*-
from collections import OrderedDict

from dateutil.relativedelta import relativedelta
from django.utils.translation import ugettext as _

from DocApproval.constants import Periods


def yes_no(bool_var):
    return _(u"Да") if bool_var else _(u"Нет")


class EnumerableGrammarFrom:
    SINGULAR = 0 #val % 10 == 1 and not val in [11;19]
    PLURAL_ONE = 1 #val % 10 in [2;4] and not val in [11;19]
    PLURAL_TWO = 2 #val %10 in 0,[5;9] or val in [11;19]

    @classmethod
    def get_enumerable_form(cls, number):
        if 11 <= number <= 19:
            return cls.PLURAL_TWO

        mod_10 = number % 10
        if mod_10 == 1:
            return cls.SINGULAR
        elif 2 <= mod_10 <= 4:
            return cls.PLURAL_ONE
        else:
            return cls.PLURAL_TWO


class Humanizer(object):
    DATE_PRECISION_DAY = 0
    DATE_PRECISION_SECOND = 1
    _period_names = OrderedDict([
        ('years', {
            EnumerableGrammarFrom.SINGULAR: _(u"год"),
            EnumerableGrammarFrom.PLURAL_ONE: _(u"года"),
            EnumerableGrammarFrom.PLURAL_TWO: _(u"лет"),
        }),
        ('months', {
            EnumerableGrammarFrom.SINGULAR: _(u"месяц"),
            EnumerableGrammarFrom.PLURAL_ONE: _(u"месяца"),
            EnumerableGrammarFrom.PLURAL_TWO: _(u"месяцев"),
        }),
        ('days', {
            EnumerableGrammarFrom.SINGULAR: _(u"день"),
            EnumerableGrammarFrom.PLURAL_ONE: _(u"дня"),
            EnumerableGrammarFrom.PLURAL_TWO: _(u"дней"),
        }),
        ('hours', {
            EnumerableGrammarFrom.SINGULAR: _(u"час"),
            EnumerableGrammarFrom.PLURAL_ONE: _(u"часа"),
            EnumerableGrammarFrom.PLURAL_TWO: _(u"часов"),
        }),
        ('minutes', {
            EnumerableGrammarFrom.SINGULAR: _(u"минута"),
            EnumerableGrammarFrom.PLURAL_ONE: _(u"минуты"),
            EnumerableGrammarFrom.PLURAL_TWO: _(u"минут"),
        }),
        ('seconds', {
            EnumerableGrammarFrom.SINGULAR: _(u"секунда"),
            EnumerableGrammarFrom.PLURAL_ONE: _(u"секунды"),
            EnumerableGrammarFrom.PLURAL_TWO: _(u"секунд"),
        })
    ])

    def get_period_name(self, name, form):
        return self._period_names.get(name, {}).get(form, "")

    def humanize_period(self, quantity, precision=DATE_PRECISION_DAY, unit=Periods.DAYS):
        delta = relativedelta(**{unit: quantity})
        attributes = self._period_names.keys()
        if precision == self.DATE_PRECISION_DAY:
            attributes.remove('hours')
            attributes.remove('minutes')
            attributes.remove('seconds')

        values = [(getattr(delta, attr), attr, EnumerableGrammarFrom.get_enumerable_form(getattr(delta, attr)))
                  for attr in attributes if getattr(delta, attr)]

        readable = (u"{0} {1}".format(value, self.get_period_name(attr, grammar_form))
                    for value, attr, grammar_form in values)

        return u" ".join(readable)