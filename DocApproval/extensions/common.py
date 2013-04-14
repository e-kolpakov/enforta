from django.utils.safestring import mark_safe

from ..messages import Common

def get_model_fields(model):
    return model._meta.fields


def render_image_from_db(image_field, css_class):
    try:
        return mark_safe("<img src='{0}' class='{1}'/>".format(image_field.url, css_class))
    except ValueError:
        return Common.IMAGE_MISSING


def render_empty_relationship():
    return "-----"