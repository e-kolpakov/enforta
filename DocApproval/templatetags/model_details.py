from django import template
from django.db import models
from ..extensions import common as common_extensions

register = template.Library()


class ModelDetailsNode(template.Node):
    def __init__(self, model, exclude_fields, child_nodes):
        self._model = model
        self._exclude_fields = exclude_fields
        self._children = child_nodes

    def _render_field(self, model, field, context):
        raw_value = getattr(model, field.name)
        if isinstance(field, models.ImageField):
            value = common_extensions.render_image_from_db(raw_value, context)
        elif isinstance(field, (models.ForeignKey, models.ManyToManyField)) and raw_value is None:
            value = common_extensions.render_empty_relationship()
        else:
            value = raw_value
        return value
        # if isinstance(value, ImageFileField)

    def render(self, context):
        model = context[self._model]
        exclude_fields = context.get(self._exclude_fields, ())
        all_fields = common_extensions.get_model_fields(model)
        fields = [field for field in all_fields if field.name not in exclude_fields]
        output = []

        classes_for_context = dict()
        if "field_caption_class" not in context:
            classes_for_context["field_caption_class"] = "field-caption"
        if "field_value_class" not in context:
            classes_for_context["field_value_class"] = "field-value"
        if "image_class" not in context:
            classes_for_context["image_class"] = "field-image"

        if len(classes_for_context) > 0:
            context.update(classes_for_context)

        for field in fields:
            sub_context = {
                'caption': field.verbose_name,
                'value': self._render_field(model, field, context['image_class'])
            }
            context.update(sub_context)
            output.append(self._children.render(context))
            context.pop()

        # cleaning up the context
        if len(classes_for_context) > 0:
            context.pop()

        return "".join(output)



@register.tag('model_details')
def  def_model_details(parser, token):
    params = token.split_contents()
    tag_name = params[0]
    if len(params) < 2:
        raise template.TemplateSyntaxError("{0} tag should have at least one argument")

    model = params[1]
    exclude_fields = params[2] if len(params) > 2 else None
    nodelist = parser.parse(("end" + tag_name, ))
    parser.delete_first_token()

    return ModelDetailsNode(model, exclude_fields, nodelist)