#-*- coding: utf-8 -*-
import logging

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from models import Permissions
from url_naming import names as url_names


class MenuException(Exception):
    ERROR_MESSAGE_TEMPLATE = _(u"Incorrect child for menu item. Expected subclass of {0}, {1} given")

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


class MenuModifierViewMixin(object):
    extender_class = None

    def _apply_extender(self, request, entity, extender_class=None):
        effective_extender_class = extender_class or self.extender_class
        extender = effective_extender_class(request)
        extender.extend(entity)


class BaseMenuItem(object):
    COMMON_MENU_ITEM_CLASS = "menu-item"
    MENU_ITEM_CLASS_DROPDOWN = "dropdown"
    MENU_ITEM_CLASS_SUBMENU = "dropdown-submenu"

    def __init__(self, children=None, css_class=None, html_id=None, parent=None, **kwargs):
        self.parent = parent
        self.css_class = self.COMMON_MENU_ITEM_CLASS
        if css_class:
            self.css_class += " " + css_class
        self.html_id = html_id
        self._children = []
        self.add_children(children if children is not None else [])
        super(BaseMenuItem, self).__init__(**kwargs)

    def add_child(self, child, order=None):
        if not isinstance(child, BaseMenuItem):
            raise MenuException(MenuException.ERROR_MESSAGE_TEMPLATE.format("BaseMenuItem", child.__class__.__name__))
        child.parent = self
        if order is None:
            self._children.append(child)
        else:
            self._children.insert(order, child)

    def add_children(self, children, continue_on_error=False):
        for child in children:
            try:
                self.add_child(child)
            except MenuException, e:
                logger = logging.getLogger(self.__class__.__name__)
                logger.exception(e.message)
                if not continue_on_error:
                    raise

    def has_children(self):
        return len(self._children) > 0

    def has_parent(self):
        return self.parent is not None

    def get_children(self):
        return self._children

    def get_dropdown_class(self):
        result = None
        if self.has_children():
            result = self.MENU_ITEM_CLASS_SUBMENU if self.has_parent() else self.MENU_ITEM_CLASS_DROPDOWN
        return result


class NavigableMixin(object):
    def __init__(self, url=None, **kwargs):
        self.url = url
        super(NavigableMixin, self).__init__(**kwargs)


class HtmlMenuItem(BaseMenuItem):
    def __init__(self, caption=None, image=None, *args, **kwargs):
        super(HtmlMenuItem, self).__init__(*args, **kwargs)
        self.caption = caption
        self.image = image

    def get_caption(self):
        return self.caption

    def get_image(self):
        return {'url': self.image}


class NavigableMenuItem(HtmlMenuItem, NavigableMixin):
    """Nothing to do here, the meat is in the superclasses"""


class MenuManager(object):
    def __init__(self, user):
        self.user = user
        self._root_items = []
        self._menu_built = False
        self._delayed_items = []

    def __iter__(self):
        for item in self.get_menu():
            yield item

    def get_menu(self):
        if not self._menu_built:
            self._build_menu()
        return self._root_items

    def add_item(self, item, order=None):
        if not self._menu_built:
            self._delayed_items.append((item, order))
        else:
            self._add_root_item(item, order)

    def _add_root_item(self, item, order=None):
        if item is not None:
            if order is None:
                self._root_items.append(item)
            else:
                self._root_items.insert(order, item)

    def _build_menu(self):
        self._add_root_item(
            NavigableMenuItem(caption=_(u"Главная"), url=reverse(url_names.Common.HOME), image="icons/home.png")
        )
        self._add_root_item(self._build_request_actions_menu())
        if self.user.has_perm(Permissions._(Permissions.ApprovalRoute.CAN_MANAGE_TEMPLATES)):
            self._add_root_item(self._build_approvals_menu())
        self._add_root_item(self._build_profile_menu())
        for item, order in self._delayed_items:
            self._add_root_item(item, order)
        self._delayed_items[:] = []
        self._menu_built = True

    def _build_request_actions_menu(self):
        root_item = HtmlMenuItem(caption=_(u"Заявки"))
        child_items = [
            NavigableMenuItem(caption=_(u"Все заявки"), image="icons/list.png", url=reverse(url_names.Request.LIST)),
        ]
        if self.user.has_perm(Permissions._(Permissions.Request.CAN_CREATE_REQUESTS)):
            child_items.insert(
                0, NavigableMenuItem(caption=_(u"Создать"), image="icons/create.png",
                                     url=reverse(url_names.Request.CREATE))
            )
            child_items.append(
                NavigableMenuItem(caption=_(u"Мои заявки"), image="icons/my_requests.png",
                                  url=reverse(url_names.Request.MY_REQUESTS))
            )

        if self.user.has_perm(Permissions._(Permissions.Request.CAN_APPROVE_REQUESTS)):
            child_items.append(
                NavigableMenuItem(caption=_(u"Ожидают утверждения"), image="icons/my_approvals.png",
                                  url=reverse(url_names.Request.MY_APPROVALS))
            )

        child_items.append(
            NavigableMenuItem(caption=_(u"Архив заявок"), image="icons/archive.png",
                              url=reverse(url_names.Request.ARCHIVE))
        )
        root_item.add_children(child_items)
        return root_item if root_item.has_children() else None

    def _build_profile_menu(self):
        root_item = NavigableMenuItem(
            caption=_(u"Ваш профиль"),
            url=reverse(url_names.Profile.PROFILE, kwargs={'pk': self.user.profile.pk}),
            children=(
                NavigableMenuItem(caption=_(u"Профиль"), image="icons/user_profile.png",
                                  url=reverse(url_names.Profile.PROFILE, kwargs={'pk': self.user.profile.pk})),
                NavigableMenuItem(caption=_(u"Редактировать"), image='icons/edit.png',
                                  url=reverse(url_names.Profile.UPDATE, kwargs={'pk': self.user.profile.pk})),
                NavigableMenuItem(caption=_(u"Выход"), image="icons/logout.png",
                                  url=reverse(url_names.Authentication.LOGOUT)),
            ))
        return root_item

    def _build_approvals_menu(self):
        root_item = HtmlMenuItem(
            caption=_(u"Шаблонные маршруты"),
            children=(
                NavigableMenuItem(caption=_(u"Создать"), image="icons/create.png",
                                  url=reverse(url_names.ApprovalRoute.TEMPLATE_CREATE)),
                NavigableMenuItem(caption=_(u"Все шаблонные маршруты"), image="icons/approval_routes_list.png",
                                  url=reverse(url_names.ApprovalRoute.LIST)),
            ))
        return root_item


class MenuManagerExtensionBase(object):
    def __init__(self, request, *args, **kwargs):
        self._user = request.user
        self._target_menu_manager = request.menu_manager
        super(MenuManagerExtensionBase, self).__init__(*args, **kwargs)

    def check_user_permissions(self, class_permissions=None, instance_permissions=None, instance=None):
        result = False
        if class_permissions:
            result = result or any(self._user.has_perm(Permissions._(perm)) for perm in class_permissions)

        if instance_permissions and instance:
            result = result or any(self._user.has_perm(Permissions._(perm), instance) for perm in instance_permissions)

        return result


class RequestContextMenuManagerExtension(MenuManagerExtensionBase):
    def extend(self, req):
        self._target_menu_manager.add_item(self._build_root_item(req), order=2)

    def _build_root_item(self, req):
        root_item = None
        child_items = []
        if self.check_user_permissions(
                class_permissions=(Permissions.Request.CAN_VIEW_ALL_REQUESTS,),
                instance_permissions=(Permissions.Request.CAN_VIEW_REQUEST,),
                instance=req):
            child_items.append(
                NavigableMenuItem(caption=_(u"Профиль"), image='icons/profile.png',
                                  url=reverse(url_names.Request.DETAILS, kwargs={'pk': req.pk}))
            )
        if self.check_user_permissions(
                instance_permissions=(Permissions.Request.CAN_EDIT_REQUEST,),
                instance=req):
            child_items.append(
                NavigableMenuItem(caption=_(u"Редактировать"), image='icons/edit.png',
                                  url=reverse(url_names.Request.UPDATE, kwargs={'pk': req.pk}))
            )
        if self.check_user_permissions(
                instance_permissions=(Permissions.Request.CAN_EDIT_ROUTE,),
                instance=req):
            child_items.append(
                NavigableMenuItem(caption=_(u"Маршрут утверждения"), image='icons/approval_route.png',
                                  url=reverse(url_names.ApprovalRoute.UPDATE, kwargs={'pk': req.approval_route.pk}))
            )
        if len(child_items) > 0:
            root_item = HtmlMenuItem(caption=_(u"Заявка"))
            root_item.add_children(child_items)
        return root_item


def menu_context_processor(request):
    manager = request.menu_manager
    return {'menu': manager}