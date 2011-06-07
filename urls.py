from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^program/', include('program.urls')),
    (r'^programm/', include('program.urls')), # programcalendar.js has to link
        # to /programm, so that deliverance integration works. that would
        # break django compat, so this url rule is added. come up with a bttr
        # solution and implement it to avoid redundancy and hacks.
        # i don't care yet.
    (r'^nop', include('nop.urls')),
    (r'^tinymce/', include('tinymce.urls')),
)
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT})
    )
