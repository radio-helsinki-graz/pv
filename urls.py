from django.conf import settings
from django.conf.urls.defaults import include, patterns
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^program/', include('program.urls')),
    (r'^tinymce/', include('tinymce.urls')),
)
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT})
    )
