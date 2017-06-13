from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve

from program.views import json_day_schedule, json_timeslots_specials

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^program/', include('program.urls')),
    url(r'^nop', include('nop.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^export/day_schedule/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', json_day_schedule),
    url(r'^export/timeslots_specials.json$', json_timeslots_specials)
]

if settings.DEBUG:
    urlpatterns.append(url(r'^site_media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}))
