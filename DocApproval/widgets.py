#-*- coding: utf-8 -*-
from django.forms import widgets
from django.utils.safestring import mark_safe

from messages import PeriodMessages


class DatePickerWidget(widgets.DateInput):
    DATEPICKER_CLASS = 'datepicker'

    def render(self, name, value, attrs=None):
        if 'class' in attrs:
            attrs['class'] += ' ' + self.DATEPICKER_CLASS
        else:
            attrs['class'] = self.DATEPICKER_CLASS
        return super(DatePickerWidget, self).render(name, value, attrs)


class PeriodSelectorWidget(widgets.TextInput):
    PERIOD_SELECTOR_CLASS = 'period_selector'
    TEMPLATE = u"""
<div class="input-append">
  {0}
  <span class='add-on'>{1}</span>
</div>
    """

    def _wrap(self, base_widget, attrs=None):
        return mark_safe(self.TEMPLATE.format(base_widget, PeriodMessages.DAYS))

    def render(self, name, value, attrs=None):
        if 'class' in attrs:
            attrs['class'] += ' ' + self.PERIOD_SELECTOR_CLASS
        else:
            attrs['class'] = self.PERIOD_SELECTOR_CLASS
        base_widget = super(PeriodSelectorWidget, self).render(name, value, attrs)
        return self._wrap(base_widget, attrs)