import django.core.files.uploadhandler as uploadhandler
import file_upload_settings

class BasicFileUploadHandler(uploadhandler.FileUploadHandler):
    file_upload_settings = None
    valid_file = True

    def __init__(self, file_upload_settings):
        if file_upload_settings is not file_upload_settings.FileUploadSettings:
            raise ValueError("file_upload_settings should be subclass of file_upload_settings.FileUploadSettings")
        self.file_upload_settings = file_upload_settings
        super(BasicFileUploadHandler).__init__()

    def receive_data_chunk(self, raw_data, start):
        if not self.valid_file:
            raise uploadhandler.StopUpload()
        return super(BasicFileUploadHandler).receive_data_chunk(raw_data, start)

    def file_complete(self, file_size):
        return super(BasicFileUploadHandler).file_complete(file_size)

    def new_file(self, field_name, file_name, content_type, content_length, charset=None):
        self.valid_file = self._match_file_type(content_type) and self._match_length_restrictions(content_length)
        if not self.valid_file:
            raise uploadhandler.StopFutureHandlers()

    def _match_file_type(self, content_type):
        return content_type in self.file_upload_settings.allowed_mime_types

    def _match_length_restrictions(self, content_length):
        return content_length <= self.file_upload_settings.max_file_size