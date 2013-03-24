from django.core.urlresolvers import reverse


class MenuItem(object):
    def __init__(self, caption, css_class=None, html_id=None, children=None):
        self.caption = caption
        self.css_class = css_class
        self.html_id = html_id
        self.children = children if children is not None else []


class NavigationMenuItem(MenuItem):
    def __init__(self, caption, url, css_class=None, html_id=None, children=None):
        super(NavigationMenuItem, self).__init__(caption, css_class=css_class, html_id=html_id, children=children)
        self.url = url


def menu_context_processor(request):
    """ Stubbed for a while """
    return {'menu': [
        MenuItem('Test1', html_id="QWE", children=(
            MenuItem("Test1.1", children=(
                MenuItem("Test1.1.1"),
                MenuItem("Test1.1.2", children=(
                    MenuItem("Test1.1.2.1"),
                ))
            )),
            MenuItem("Test1.2")
        )),
        MenuItem('Test2', css_class="ASD"),
        NavigationMenuItem("To quicktest", reverse("common.quick_test"), children=(
            MenuItem("Nav1.1"),
            MenuItem("Nav1.2"),
        ))
    ]}