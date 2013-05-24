__author__ = 'john'


# Prevent interactive question about wanting a superuser created.  (This
# code has to go in this otherwise empty "models" module so that it gets
# processed by the "syncdb" command during database creation.)

from django.db.models import signals
from django.contrib.auth.management import create_superuser
from django.contrib.auth import models as auth_app

signals.post_syncdb.disconnect(
    create_superuser,
    sender=auth_app,
    dispatch_uid="django.contrib.auth.management.create_superuser")

from common import Position, City
from approval import ApprovalRoute, ApprovalRouteStep, ApprovalProcess, ApprovalProcessAction, NonTemplateApprovalRouteException
from request import Request, RequestStatus, Permissions, RequestFactory, Contract
from user import UserProfile