#-*- coding: utf-8 -*-
def get_url_base(url):
    return "/".join(url.split('/')[:-1])


def reprint_form_errors(errors):
    return tuple(u"{0}: {1}".format(key, u";".join(value)) for key, value in errors.items())