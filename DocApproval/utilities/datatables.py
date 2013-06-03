from django.core.exceptions import ImproperlyConfigured
from django_datatables_view.base_datatable_view import BaseDatatableView


class ColumnDefinition(object):
    def __init__(self, column, name, is_calculated=False, link_config=None):
        self.column = column
        self.name = name
        self.is_calculated = is_calculated
        self.link_config = link_config

    def to_dict(self):
        result = {
            'column': self.column,
            'name': self.name,
            'is_calculated': self.is_calculated
        }
        if self.link_config:
            result['link_config'] = self.link_config
        return result


class JsonConfigurableDatatablesBaseView(BaseDatatableView):
    CONFIG_MARKER = 'config'

    model = None
    display_fields = ()
    model_fields = ()
    calculated_fields = {}
    link_target = None
    link_field = None

    def get_link_url(self):
        link = self.link_target
        return link() if hasattr(link, '__call__') else link

    def get_model_fields(self):
        return self.model_fields

    def get_display_fields(self):
        return self.get_model_fields() + tuple(self.get_calculated_fields().keys())

    def get_calculated_fields(self):
        return self.calculated_fields

    def get_order_columns(self):
        return self.get_display_fields()

    def prepare_single_item(self, item):
        return item.__dict__

    def get_model_columns(self):
        return {f.name: f.verbose_name for f in self.model._meta.local_fields}

    def get_context_data(self, *args, **kwargs):
        if kwargs.get(self.CONFIG_MARKER, False):
            return self.get_config(**kwargs)
        else:
            return super(JsonConfigurableDatatablesBaseView, self).get_context_data(self, *args, **kwargs)

    def get_columns_config(self):
        columns = []
        links_config = self.get_links_config()
        for field in self.get_model_fields():
            field_def = self.model._meta.get_field_by_name(field)[0]
            if field_def is None:
                raise ImproperlyConfigured("Field {0} not found for model {1}".format(field, self.model.__class__.name))
            col_def = ColumnDefinition(field, field_def.verbose_name, is_calculated=False,
                                       link_config=links_config.get(field, None))
            columns.append(col_def)
        for field, caption in self.get_calculated_fields().iteritems():
            col_def = ColumnDefinition(field, caption, is_calculated=True,
                                       link_config=links_config.get(field, None))
            columns.append(col_def)

        column_order = self.get_order_columns()
        columns.sort(key=lambda col: column_order.index(col.column))
        return [col.to_dict() for col in columns]

    def get_links_config(self):
        return None

    def get_config(self, **kwargs):
        return {
            'columns': self.get_columns_config()
        }

    def prepare_results(self, qs):
        return [self.prepare_single_item(item) for item in qs]