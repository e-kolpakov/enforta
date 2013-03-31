#-*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

import logging
from models import Permissions
from url_naming import names as url_names


class MenuException(Exception):
    ERROR_MESSAGE_TEMPLATE = _(u"Incorrect child for menu item. Expected subclass of {0}, {1} given")

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


class BaseMenuItem(object):
    COMMON_MENU_ITEM_CLASS = "menu-item"

    def __init__(self, children=None, css_class=None, html_id=None, *args, **kwargs):
        self.css_class = self.COMMON_MENU_ITEM_CLASS
        if css_class:
            self.css_class += " " + css_class
        self.html_id = html_id
        self._children = children if children is not None else []
        super(BaseMenuItem, self).__init__(*args, **kwargs)

    def add_child(self, child):
        if not isinstance(child, BaseMenuItem):
            raise MenuException(MenuException.ERROR_MESSAGE_TEMPLATE.format("BaseMenuItem", child.__class__.__name__))
        self._children.append(child)

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

    def get_children(self):
        return self._children


class NavigableMixin(object):
    def __init__(self, url=None, *args, **kwargs):
        self.url = url
        super(NavigableMixin, self).__init__(*args, **kwargs)


class HtmlMenuItem(BaseMenuItem):
    def __init__(self, caption=None, image=None, image_class=None, *args, **kwargs):
        super(HtmlMenuItem, self).__init__(*args, **kwargs)
        self.caption = caption
        self.image = image
        self.image_class = image_class

    def get_caption(self):
        return self.caption

    def get_image(self):
        return {'url': self.image, 'class': self.image_class}


class NavigableMenuItem(HtmlMenuItem, NavigableMixin):
    """Nothing to do here, the meat is in the superclasses"""


class MenuManager(object):
    def __init__(self, user):
        self.user = user
        self._root_items = []
        self._menu_built = False

    def get_menu(self):
        if not self._menu_built:
            self._build_menu()
        return self._root_items

    def _add_root_item(self, item):
        if item is not None:
            self._root_items.append(item)

    def _build_menu(self):
        self._add_root_item(
            NavigableMenuItem(caption=_(u"Главная"), url=reverse(url_names.Common.HOME), image="icons/home.png")
        )
        self._add_root_item(self._build_request_actions_menu())
        self._add_root_item(self._build_profile_menu())

    def _build_request_actions_menu(self):
        root_item = HtmlMenuItem(caption=_(u"Заявки"))
        child_items = [
            NavigableMenuItem(caption=_(u"Все заявки"), image="icons/list.png", url=reverse(url_names.Request.LIST)),
        ]
        if self.user.has_perm(Permissions.Request.CAN_CREATE_REQUESTS):
            child_items.insert(
                0, NavigableMenuItem(caption=_(u"Создать"), image="icons/create.png",
                                     url=reverse(url_names.Request.CREATE))
            )
            child_items.append(
                NavigableMenuItem(caption=_(u"Мои заявки"), image="icons/my_requests.png",
                                  url=reverse(url_names.Request.MY_REQUESTS))
            )

        if self.user.has_perm(Permissions.Request.CAN_APPROVE_REQUESTS):
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
            caption=self.user.username, url=reverse(url_names.Profile.PROFILE),
            children=(
                NavigableMenuItem(caption=_(u"Профиль"), image="icons/user_profile.png",
                                  url=reverse(url_names.Profile.PROFILE)),
                NavigableMenuItem(caption=_(u"Выход"), image="icons/logout.png",
                                  url=reverse(url_names.Authentication.LOGOUT)),
            ))
        return root_item


def menu_context_processor(request):
    manager = MenuManager(request.user)

    return {'menu': manager.get_menu()}

    # return {'menu': (
    #     HtmlMenuItem(caption='Test1', html_id="QWE", children=(
    #         HtmlMenuItem(caption="Test1.1", children=(
    #             HtmlMenuItem(caption="Test1.1.1"),
    #             HtmlMenuItem(caption="Test1.1.2", children=(
    #                 HtmlMenuItem(caption="Test1.1.2.1"),
    #             ))
    #         )),
    #         HtmlMenuItem(caption="Test1.2")
    #     )),
    #     HtmlMenuItem(caption='Test2', css_class="ASD", image="home.png"),
    #     NavigableMenuItem(caption="To quicktest", url=reverse("common.quick_test"), children=(
    #         HtmlMenuItem(caption="Nav1.1"),
    #         HtmlMenuItem(caption="Nav1.2"),
    #     ))
    # )}