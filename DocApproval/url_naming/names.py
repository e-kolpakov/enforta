class _NamesMeta(type):
    def __new__(mcs, name, bases, dct):
        modified_dict = {
            key: ".".join((name.lower(), value))
            for key, value in dct.items() if not key.startswith('__')
        }
        return super(_NamesMeta, mcs).__new__(_NamesMeta, name, bases, modified_dict)


class Common:
    __metaclass__ = _NamesMeta
    HOME = "home_page"


class Authentication:
    __metaclass__ = _NamesMeta
    LOGIN = "login"
    LOGOUT = "logout"


class Request:
    __metaclass__ = _NamesMeta
    LIST = "all_list"
    CREATE = "create"
    DETAILS = "details"
    MY_REQUESTS = "my_requests_list"
    MY_APPROVALS = "my_approval_list"

    ARCHIVE = "archive"
    ARCHIVE_YEAR = "archive.year"
    ARCHIVE_MONTH = "archive.month"


class Profile:
    __metaclass__ = _NamesMeta
    PROFILE = "profile"