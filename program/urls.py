from django.conf.urls.defaults import *

from django.views.generic.list_detail import object_detail, object_list

from models import Host, Show, TimeSlot
from views import current_show, day_schedule, recommendations, show_list, today_schedule, week_schedule

urlpatterns = patterns('',
    ('^$', today_schedule),
    ('^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', day_schedule),
    ('^(?P<year>\d{4})/(?P<week>\d{1,2})/$', week_schedule),
    ('^current_box/$', current_show),
    ('^hosts/$', object_list, dict(template_object_name='host', queryset=Host.objects.all())),
    url('^host/(?P<object_id>\d+)/$', object_detail, dict(template_object_name='host', queryset=Host.objects.all()), name='host-detail'),
    ('^recommendations/$', recommendations),
    ('^recommendations_box/$', recommendations, dict(template_name='program/recommendations_box.html')),
    ('^shows/$', show_list),
    url('^show/(?P<slug>[\w-]+)/$', object_detail, dict(template_object_name='show', queryset=Show.objects.all()), name='show-detail'),
    url('^(?P<object_id>\d+)/$', object_detail, dict(template_object_name='timeslot', queryset=TimeSlot.objects.all()), name='timeslot-detail'),
)
