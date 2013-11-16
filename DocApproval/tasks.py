# -*- coding=utf-8 -*-
import logging
from celery import task

from DocApproval.models import Request


logger = logging.getLogger(__name__)

@task()
def archive_requests():
    logger.debug("Starting archive_request")
    target_requests = Request.objects.get_expired_requests()
    logger.debug("Requests fetched")

    for request in target_requests:
        request.set_expired()

    logger.debug("Requests archived")
    logger.debug("Total {0} requests processed".format(len(target_requests)))