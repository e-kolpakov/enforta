from django.forms import widgets


class DatePickerWidget(widgets.DateInput):
    def render(self, name, value, attrs=None):
        if 'class' in attrs:
            attrs['class'] += ' datepicker'
        else:
            attrs['class'] = 'datepicker'
        return super(DatePickerWidget, self).render(name, value, attrs)