from django.conf.urls import patterns, url
from names import Media as media_names

from ..views import media

urlpatterns = patterns(
    '',
    url(r"(?P<filename>.*)", media.media, name=media_names.MEDIA),
)