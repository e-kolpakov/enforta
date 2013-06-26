#-*- coding: utf-8 -*-
import logging
import magic

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

import django.core.files.uploadhandler as upload_handler
from django.conf import settings

from django.db.models import FileField
from django.forms import forms
from django.template.defaultfilters import filesizeformat

from DocApproval.messages import RequestMessages


_logger = logging.getLogger(__name__)


def get_file_type(incoming_file):
    ordinary_type = incoming_file.content_type
    if settings.USE_MAGIC and ordinary_type in settings.SKIP_MAGIC_FILE_TYPES:
        _logger.debug("Skipping file {0} from magic")

    if settings.USE_MAGIC and ordinary_type not in settings.SKIP_MAGIC_FILE_TYPES:
        _logger.debug("Beware, using MAGIC!")
        try:
            incoming_file.open('r')
            buf = incoming_file.read(1024)
        finally:
            incoming_file.close()

        magic_type = magic.from_buffer(buf, mime=True)
        _logger.debug(
            "Ok, magic said that it is {0}, and file itself says it is {1}".
            format(magic_type, ordinary_type)
        )
        result = magic_type
    else:
        result = ordinary_type
    return result.lower()


class BasicFileUploadHandler(upload_handler.FileUploadHandler):
    allowed_mime_types = settings.ALLOWED_MIME_TYPES

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


class ContentTypeRestrictedFileField(FileField):
    def __init__(self, *args, **kwargs):
        self.content_types = settings.ALLOWED_MIME_TYPES
        self.max_upload_size = settings.MAX_FILE_SIZE * 1024

        super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ContentTypeRestrictedFileField, self).clean(*args, **kwargs)

        incoming_file = data.file
        try:
            content_type = get_file_type(incoming_file)
            if content_type in self.content_types:
                if incoming_file._size > self.max_upload_size:
                    max_file_size = filesizeformat(self.max_upload_size)
                    current_file_size = filesizeformat(incoming_file._size)
                    msg = RequestMessages.FILE_IS_TOO_BIG.format(current_file_size, max_file_size)
                    raise forms.ValidationError(msg)
            else:
                raise forms.ValidationError(RequestMessages.FILE_TYPE_IS_NOT_SUPPORTED.format(content_type))
        except AttributeError:
            raise

        return data