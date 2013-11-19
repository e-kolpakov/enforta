import json
import datetime
from django.http import HttpResponse
from Utilities.humanization import Humanizer


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S %z')
        if isinstance(obj, datetime.timedelta):
            return Humanizer().humanize_timedelta(obj, Humanizer.DATE_PRECISION_SECOND)
        return json.JSONEncoder.default(self, obj)


class JsonViewMixin(object):
    def _get_json_response(self, callback, *args, **kwargs):
        try:
            data = callback(*args, **kwargs)
            data = {
                'success': True,
                'data': data
            }
        except Exception as e:
            if hasattr(self, '_logger'):
                self._logger.exception("Exception while performing ajax request")
            data = {
                'success': False,
                'error': [str(e)],
                'data': None
            }
        return HttpResponse(json.dumps(data, cls=CustomJsonEncoder), content_type="application/json")
