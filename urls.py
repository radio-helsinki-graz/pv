from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

import os

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^program/', include('helsinki.program.urls')),
)
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$',
         'django.views.static.serve',
         {'document_root': os.path.join(os.path.dirname(__file__), 'site_media')}
        ),
    )
