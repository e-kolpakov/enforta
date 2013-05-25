import logging


class RequestStatusManager(object):
    _logger = logging.getLogger(__name__ + ".RequestStatusManager")

    def __init__(self, instance):
        self._instance = instance

    def handle_status_update(self, old_status, new_status):
        self._logger.debug(
            u"Handling status change on instance {0} - {1} => {2}".format(self._instance, old_status, new_status))