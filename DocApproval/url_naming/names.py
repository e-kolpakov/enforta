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
    CREATE = "create"
    LIST = "all_list" #aka (R)equest
    LIST_JSON = "list_json"
    LIST_JSON_CONF = "list_json_conf"
    UPDATE = "edit"
    DETAILS = "details"
    MY_REQUESTS = "my_requests_list"
    MY_APPROVALS = "my_approval_list"

    ARCHIVE = "archive"
    ARCHIVE_YEAR = "archive_year"
    ARCHIVE_MONTH = "archive_month"


class ApprovalRoute:
    __metaclass__ = _NamesMeta
    CREATE = "create"
    REQUEST = "request"
    UPDATE = "update"


class Profile:
    __metaclass__ = _NamesMeta
    PROFILE = "profile"
    MY_PROFILE = "my_profile"
    UPDATE = "edit"