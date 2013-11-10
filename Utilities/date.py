import re
from datetime import timedelta

_date_regex = re.compile(r'^(?:(?P<days>\d+)\sdays?)?(?:,\s)?(?:(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d+))?$')

def parse_string_to_timedelta(string):
    """Parses the default timedelta string representation back to timedelta object"""
    d = _date_regex.match(string).groupdict(0)
    return timedelta(**dict(((key, int(value)) for key, value in d.items())))