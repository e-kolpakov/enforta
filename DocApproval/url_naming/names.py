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
    UPDATE = "edit"
    DETAILS = "details"

    LIST = "all_list"
    MY_REQUESTS = "my_requests_list"
    MY_APPROVALS = "my_approval_list"

    LIST_JSON = "list_json"
    LIST_JSON_CONF = "list_json_conf"
    ACTIONS_BACKEND_JSON = "actions"

    APPROVAL_HISTORY = "approval_history"
    APPROVAL_SHEET = "approval_sheet"

    ARCHIVE = "archive"
    ARCHIVE_YEAR = "archive_year"
    ARCHIVE_MONTH = "archive_month"


class ApprovalRoute:
    __metaclass__ = _NamesMeta
    CREATE = "create"
    LIST = "list" #aka (R)equest
    UPDATE = "update"

    TEMPLATE_CREATE = "template.create"
    TEMPLATE_EDIT = "template.edit"

    LIST_JSON = "list_json"
    LIST_JSON_CONF = "list_json_conf"

    APPROVERS_JSON = "approvers_json"
    TEMPLATES_JSON = "templates_json"
    APPROVAL_ROUTE_BACKEND_JSON = "approval_route_backend_json"


class Profile:
    __metaclass__ = _NamesMeta
    PROFILE = "profile"
    MY_PROFILE = "my_profile"
    UPDATE = "edit"


class Media:
    __metaclass__ = _NamesMeta
    MEDIA = "media"