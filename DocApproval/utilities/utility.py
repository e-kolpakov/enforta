import re
import dateutil.parser


def get_url_base(url):
    return "/".join(url.split('/')[:-1])


def reprint_form_errors(errors):
    return tuple(u"{0}: {1}".format(key, u";".join(value)) for key, value in errors.items())


def parse_string_to_datetime(string):
    return dateutil.parser.parse(string, dayfirst=True)


def public_view(func):
    func.is_public = True
    return func


def wrap_permission(permission, app_label='DocApproval'):
    """Adds app_label to requested permission"""
    return app_label + "." + permission