import logging
from collections import OrderedDict

from django.core.exceptions import ImproperlyConfigured
from django.db.models.fields import FieldDoesNotExist
from django_datatables_view.base_datatable_view import BaseDatatableView

_logger = logging.getLogger(__name__)


class ColumnDefinition(object):
    is_virtual = False
    column_type = None

    def __init__(self, column='', name='', order=0, is_calculated=False):
        self.column = column
        self.name = name
        self.is_calculated = is_calculated
        self.order = order

    def to_dict(self):
        result = {
            'column': self.column,
            'name': self.name,
            'is_calculated': self.is_calculated,
            'is_virtual': self.is_virtual,
            'column_type': self.column_type
        }
        return result


class ModelField(ColumnDefinition):
    column_type = 'model_field_column'

    def __init__(self, field, model, **kwargs):
        try:
            field_def = model._meta.get_field_by_name(field)[0]
            super(ModelField, self).__init__(column=field, name=field_def.verbose_name, **kwargs)
        except FieldDoesNotExist as e:
            _logger.exception(e)
            raise ImproperlyConfigured("Field {0} not found for model {1}".format(field, model.__class__.name))


class LinkColumnDefinition(ModelField):
    column_type = 'link_column'

    def __init__(self, base_url, entity_key='pk', *args, **kwargs):
        self.base_url = base_url
        self.entity_key = entity_key
        super(LinkColumnDefinition, self).__init__(*args, **kwargs)

    def to_dict(self):
        sup = super(LinkColumnDefinition, self).to_dict()
        sup['specification'] = {'base_url': self.base_url, 'entity_key': self.entity_key}
        return sup


class CheckboxColumnDefinition(ColumnDefinition):
    is_virtual = True
    column_type = 'checkbox_column'

    def __init__(self, entity_key, **kwargs):
        super(CheckboxColumnDefinition, self).__init__(**kwargs)
        self.entity_key = entity_key

    def to_dict(self):
        sup = super(CheckboxColumnDefinition, self).to_dict()
        sup['specification'] = {'entity_key': self.entity_key}
        return sup


class ActionsColumnDefintion(ColumnDefinition):
    is_virtual = True
    column_type = 'actions_column'

    def __init__(self, actions, backend_url, *args, **kwargs):
        self.actions = actions
        self.backend_url = backend_url
        super(ActionsColumnDefintion, self).__init__(*args, **kwargs)

    def to_dict(self):
        sup = super(ActionsColumnDefintion, self).to_dict()
        sup['specification'] = [
            {'icon': action.icon, 'code': action.code, 'backend_url': self.backend_url}
            for action in self.actions
        ]
        return sup


class JsonConfigurableDatatablesBaseView(BaseDatatableView):
    CONFIG_MARKER = 'config'

    model = None
    model_fields = ()

    def get_context_data(self, *args, **kwargs):
        if kwargs.get(self.CONFIG_MARKER, False):
            return self.get_config(**kwargs)
        else:
            return super(JsonConfigurableDatatablesBaseView, self).get_context_data(self, *args, **kwargs)

    def get_model_columns(self):
        return {field: ModelField(field, self.model, order=idx * 10) for idx, field in enumerate(self.model_fields)}

    def get_other_columns(self):
        return OrderedDict()

    def get_columns_config(self):
        columns = self.get_model_columns()
        columns.update(self.get_other_columns())
        cols = columns.values()
        cols.sort(key=lambda x: x.order)
        return [col.to_dict() for col in cols]

    def get_buttons_config(self):
        return None

    def get_config(self, **kwargs):
        return {
            'columns': self.get_columns_config(),
            'buttons': self.get_buttons_config()
        }

    def prepare_single_item(self, item):
        return item.__dict__

    def prepare_results(self, qs):
        return [self.prepare_single_item(item) for item in qs]