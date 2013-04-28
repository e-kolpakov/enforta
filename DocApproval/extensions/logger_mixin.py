__author__ = 'john'

import logging


class LoggableMixin(object):
    def __init__(self, *args, **kwargs):
        super(LoggableMixin, self).__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__ + "." + self.__class__.__name__)
        self.log_level_mapping = {
            logging.DEBUG: self.logger.debug,
            logging.INFO: self.logger.info,
            logging.WARN: self.logger.warn,
            logging.ERROR: self.logger.error,
            logging.FATAL: self.logger.fatal,
            logging.CRITICAL: self.logger.critical
        }

    def log(self, message, log_level, *args, **kwargs):
        log_callee = self.log_level_mapping.get(log_level, None)
        if log_level is None:
            self.logger.warn("Unknown logging level {0}".format(log_level))
        else:
            log_callee(message, *args, **kwargs)
