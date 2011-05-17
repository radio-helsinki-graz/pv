from django.conf.urls.defaults import *
from views import get, get_current, nop_form

urlpatterns = patterns('',
    url(r'^get_current/?$', get_current),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<hour>\d{1,2})/(?P<minute>\d{1,2})/?$', get),
    url(r'^$', nop_form),
)
