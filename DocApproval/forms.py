from django import forms
from models import Position
import widgets


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
    qweqwe = forms.DateField(widget=widgets.DatepickerWidget)