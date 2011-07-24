from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail, object_list

from models import Host, Show, TimeSlot
from views import current_show, day_schedule, recommendations, show_list, week_schedule

from datetime import date

hosts_dict = {
    'queryset': Host.objects.filter(shows__programslots__until__gte=date.today()).distinct(),
    'template_object_name': 'host'
}
shows_dict = {
    'queryset': Show.objects.filter(programslots__until__gt=date.today()).exclude(id=1).distinct(),
    'template_object_name': 'show'
}
timeslots_dict = {
    'queryset': TimeSlot.objects.all(),
    'template_object_name': 'timeslot'
}
recommendations_dict = {'template_name': 'program/boxes/recommendations.html'}

urlpatterns = patterns('',
    url(r'^today/?$', day_schedule),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/?$', day_schedule),
    url(r'^(?P<year>\d{4})/(?P<week>\d{1,2})/?$', week_schedule),
    url(r'^current_box/?$', current_show),
    url(r'^hosts/?$', object_list, hosts_dict),
    url(r'^hosts/(?P<object_id>\d+)/?$', object_detail, hosts_dict, name='host-detail'),
    url(r'^tips/?$', recommendations),
    url(r'^tips_box/?$', recommendations, recommendations_dict),
    url(r'^shows/?$', show_list),
    url(r'^shows/(?P<slug>[\w-]+)/?$', object_detail, shows_dict, name='show-detail'),
    url(r'^(?P<object_id>\d+)/?$', object_detail, timeslots_dict, name='timeslot-detail'),
    url(r'^week/?$', week_schedule),
)

if settings.DEBUG:
    import os
    PROGRAM_STATIC_DIR = os.path.join(os.path.dirname(__file__), '../site_media')
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': PROGRAM_STATIC_DIR}),
    )
