#-*- coding: utf-8 -*-
from collections import OrderedDict

from dateutil.relativedelta import relativedelta
from django.utils.translation import ugettext as _

from DocApproval.constants import Periods


def yes_no(bool_var):
    return _(u"Да") if bool_var else _(u"Нет")


class EnumerableGrammarForm:
    SINGULAR = 0    # val % 10 == 1 and not val in [11;19]
    PLURAL_ONE = 1  # val % 10 in [2;4] and not val in [11;19]
    PLURAL_TWO = 2  # val %10 in 0,[5;9] or val in [11;19]

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
    DATE_PRECISION_HOUR = 1
    DATE_PRECISION_MINUTE = 2
    DATE_PRECISION_SECOND = 3

    _period_names = OrderedDict([
        ('years', {
            EnumerableGrammarForm.SINGULAR: _(u"год"),
            EnumerableGrammarForm.PLURAL_ONE: _(u"года"),
            EnumerableGrammarForm.PLURAL_TWO: _(u"лет"),
        }),
        ('months', {
            EnumerableGrammarForm.SINGULAR: _(u"месяц"),
            EnumerableGrammarForm.PLURAL_ONE: _(u"месяца"),
            EnumerableGrammarForm.PLURAL_TWO: _(u"месяцев"),
        }),
        ('days', {
            EnumerableGrammarForm.SINGULAR: _(u"день"),
            EnumerableGrammarForm.PLURAL_ONE: _(u"дня"),
            EnumerableGrammarForm.PLURAL_TWO: _(u"дней"),
        }),
        ('hours', {
            EnumerableGrammarForm.SINGULAR: _(u"час"),
            EnumerableGrammarForm.PLURAL_ONE: _(u"часа"),
            EnumerableGrammarForm.PLURAL_TWO: _(u"часов"),
        }),
        ('minutes', {
            EnumerableGrammarForm.SINGULAR: _(u"минута"),
            EnumerableGrammarForm.PLURAL_ONE: _(u"минуты"),
            EnumerableGrammarForm.PLURAL_TWO: _(u"минут"),
        }),
        ('seconds', {
            EnumerableGrammarForm.SINGULAR: _(u"секунда"),
            EnumerableGrammarForm.PLURAL_ONE: _(u"секунды"),
            EnumerableGrammarForm.PLURAL_TWO: _(u"секунд"),
        })
    ])

    _default_period_for_precision = {
        DATE_PRECISION_DAY: 'days',
        DATE_PRECISION_HOUR: 'hours',
        DATE_PRECISION_MINUTE: 'minutes',
        DATE_PRECISION_SECOND: 'seconds',
    }

    def get_period_name(self, name, form):
        return self._period_names.get(name, {}).get(form, "")

    def _humanize(self, delta, precision):
        attributes = self._period_names.keys()
        if precision <= self.DATE_PRECISION_MINUTE:
            attributes.remove('seconds')
        if precision <= self.DATE_PRECISION_HOUR:
            attributes.remove('minutes')
        if precision <= self.DATE_PRECISION_DAY:
            attributes.remove('hours')

        values = [(getattr(delta, attr), attr, EnumerableGrammarForm.get_enumerable_form(getattr(delta, attr)))
                  for attr in attributes if getattr(delta, attr)]

        readable = [
            u"{quantity} {unit}".format(quantity=value, unit=self.get_period_name(attr, grammar_form))
            for value, attr, grammar_form in values
        ]

        if not readable:
            period = self.get_period_name(self._default_period_for_precision.get(precision, 'days'),
                                          EnumerableGrammarForm.PLURAL_TWO)
            readable.append(u"{quantity} {unit}".format(quantity=0, unit=period))

        return u" ".join(readable)

    def humanize_timedelta(self, timedelta, precision=DATE_PRECISION_DAY):
        """
        @type timedelta : datetime.timedelta
        @rtype: str
        """
        delta = relativedelta(days=timedelta.days, seconds=timedelta.seconds, microseconds=timedelta.microseconds)
        return self._humanize(delta, precision)

    def humanize_period(self, quantity, unit=Periods.DAYS, precision=DATE_PRECISION_DAY):
        delta = relativedelta(**{unit: quantity})
        return self._humanize(delta, precision)