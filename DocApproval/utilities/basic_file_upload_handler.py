import logging

import django.core.files.uploadhandler as upload_handler
from django.conf import settings


_logger = logging.getLogger(__name__)


class BasicFileUploadHandler(upload_handler.FileUploadHandler):
    allowed_mime_types = (
        'application/pdf',
        'application/x-pdf',
        'Image/tiff',
        'image/x-tiff',
        'Image/jpeg',
        'image/pjpeg',
        'application/msword',
        'application/excel',
        'application/vnd.ms-excel',
        'application/x-excel',
        'application/x-msexcel',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    _uploading_files_sizes = dict()

    def __init__(self, *args, **kwargs):
        self.valid_file = True
        super(BasicFileUploadHandler, self).__init__(*args, **kwargs)

    def receive_data_chunk(self, raw_data, start):
        if not self.valid_file:
            _logger.debug("Invalid file - stoppping upload")
            raise upload_handler.SkipFile()
        return raw_data

    def file_complete(self, file_size):
        return None

    def new_file(self, field_name, file_name, content_type, content_length, charset=None):
        self.valid_file = self.valid_file and self._match_file_type(content_type)
        if not self.valid_file:
            _logger.debug("Invalid file - stoppping upload")
            raise upload_handler.StopFutureHandlers()

    def handle_raw_input(self, input_data, META, content_length, boundary, encoding=None):
        self.valid_file = self._match_length_restrictions(content_length)
        return None

    def _match_file_type(self, content_type):
        _logger.debug("Checking content type {0}".format(content_type))
        return content_type in self.allowed_mime_types

    def _match_length_restrictions(self, content_length):
        _logger.debug("File size is {0}".format(content_length))
        return content_length <= settings.MAX_FILE_SIZE * 1024