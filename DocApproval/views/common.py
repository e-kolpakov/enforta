from django.shortcuts import render
from django.views.generic import TemplateView
from DocApproval.models import Groups, Request


class HomePagePartBase(object):
    show_to_groups = ()
    template = None
    id = None

    def should_show(self, user, user_groups):
        return set(user_groups) & set(self.show_to_groups)

    def get_template_data(self, request):
        return None


class MyRequestsHomePagePart(HomePagePartBase):
    show_to_groups = (Groups.USERS, )
    template = "home_page/my_approvals.html"
    id = 'my_approvals'

    def get_template_data(self, request):
        return Request.objects.get_accessible_requests(request.user)


class HomePage(TemplateView):
    _parts = (MyRequestsHomePagePart, )

    def _get_parts(self, request):
        groups = [group.name for group in request.user.groups.all()]
        result = []
        for part_class in self._parts:
            part = part_class()
            if part.should_show(request.user, groups):
                result.append((part.template, part.get_template_data(request), part.id))
        return result

    def get(self, request, *args, **kwargs):
        return render(request, "home_page/index.html", {'parts': self._get_parts(request)})

