#-*- coding: utf-8 -*-
import os

from django import template
from django.utils.encoding import smart_str
from django.utils.translation import ugettext as _


register = template.Library()

@register.simple_tag
def yes_no(variable, yes_text = _(u"Да"), no_text=_(u"Нет")):
    return yes_text if variable else no_text

@register.filter(name='filename')
def filename(value):
    return smart_str(os.path.basename(value.name))