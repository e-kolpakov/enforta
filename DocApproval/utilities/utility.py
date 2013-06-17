import re
from datetime import timedelta
import dateutil.parser

_date_regex = re.compile(r'^(?:(?P<days>\d+)\sdays?,\s)?(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d+)$')


def get_url_base(url):
    return "/".join(url.split('/')[:-1])


def reprint_form_errors(errors):
    return tuple(u"{0}: {1}".format(key, u";".join(value)) for key, value in errors.items())


def parse_string_to_timedelta(string):
    """Parses the default timedelta string representation back to timedelta object"""
    d = _date_regex.match(string).groupdict(0)
    return timedelta(**dict(((key, int(value)) for key, value in d.items())))


def parse_string_to_datetime(string):
    return dateutil.parser.parse(string, dayfirst=True)


def public_view(func):
    func.is_public = True
    return func