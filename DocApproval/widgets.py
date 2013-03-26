from django.forms import widgets


class DatepickerWidget(widgets.DateInput):
    def render(self, name, value, attrs=None):
        if 'class' in attrs:
            attrs['class'] += ' datepicker'
        else:
            attrs['class'] = 'datepicker'
        return super(DatepickerWidget, self).render(name, value, attrs)