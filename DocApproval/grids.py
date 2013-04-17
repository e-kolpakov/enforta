from django.db.models import Model
from django.core.urlresolvers import ( reverse_lazy)
from django.core.serializers.json import DjangoJSONEncoder

from models import Request
from extensions.jqgrid import JqGrid
from url_naming.names import Request as RequestUrls


def get_url_base(view):
    return "/".join(view.split('/')[:-1])


class PartialJsonEncoder(DjangoJSONEncoder):
    def __init__(self, already_encoded=None, *args, **kwargs):
        super(PartialJsonEncoder, self).__init__(*args, **kwargs)
        self._already_encoded = already_encoded if already_encoded else ()

    def default(self, obj):
        return super(PartialJsonEncoder, self).default(obj)


class RequestGrid(JqGrid):
    model = Request
    url = reverse_lazy(RequestUrls.LIST_JSON)
    caption = ""
    hide_pk = True
    editable = False
    follow_foreign_keys = True

    colmodel_overrides = {
        'name': {'formatter': "restfullink",
                 'url_base': lambda: get_url_base(reverse_lazy(RequestUrls.DETAILS, kwargs={'pk': 0}))}
    }

    def prepare_entity(self, entity):
        def serialize_field(field):
            value = getattr(entity, field)
            if isinstance(value, Model):
                return str(value)
            else:
                return value

        return {
            field: serialize_field(field)
            for field in self.get_field_names()
        }