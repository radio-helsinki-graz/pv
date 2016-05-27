from django.conf import settings
from django.conf.urls import patterns, url, include
from django.contrib import admin

from program.views import json_day_schedule

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^program/', include('program.urls')),
                       url(r'^nop', include('nop.urls')),
                       url(r'^tinymce/', include('tinymce.urls')),
                       url(r'^export/day_schedule/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', json_day_schedule)
                       )

if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
                             {'document_root': settings.MEDIA_ROOT})
                            )
