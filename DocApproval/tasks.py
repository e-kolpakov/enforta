# -*- coding=utf-8 -*-
from celery import task
import logging

from DocApproval.models import Request, RequestStatus


logger = logging.getLogger(__name__)

@task()
def archive_requests():
    logger.debug("Starting archive_request")
    target_requests = Request.objects.get_expired_requests()
    logger.debug("Requests fetched")
    target_status = RequestStatus.objects.get(pk=RequestStatus.EXPIRED)

    for request in target_requests:
        request.status = target_status
        request.save()

    logger.debug("Requests archived")
    logger.debug("Total %s requests processed", len(target_requests))