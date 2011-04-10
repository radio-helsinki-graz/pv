from django.conf.urls.defaults import *

from django.views.generic.list_detail import object_detail, object_list

from models import BroadcastFormat, Host, Show, TimeSlot
from views import current_show, day_schedule, recommendations, show_list, week_schedule

host_dict = {
    'queryset': Host.objects.all(),
    'template_object_name': 'host'
}
show_dict = {
    'queryset': Show.objects.all(),
    'template_object_name': 'show'
}
timeslot_dict = {
    'queryset': TimeSlot.objects.all(),
    'template_object_name': 'timeslot'
}
broadcastformart_dict = {
    'queryset': BroadcastFormat.objects.all(),
    'template_name': 'program/broadcastformats_box.html',
    'template_object_name': 'broadcastformat'
}
recommendation_dict = {'template_name': 'program/recommendations_box.html'}

urlpatterns = patterns('',
    (r'^today/?$', day_schedule),
    (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/?$', day_schedule),
    (r'^(?P<year>\d{4})/(?P<week>\d{1,2})/?$', week_schedule),
    (r'^current_box/?$', current_show),
    (r'^hosts/?$', object_list, host_dict),
    url(r'^hosts/(?P<object_id>\d+)/?$', object_detail, host_dict, name='host-detail'),
    (r'^tips/?$', recommendations),
    (r'^tips_box/?$', recommendations, recommendation_dict),
    (r'^shows/?$', show_list),
    url(r'^shows/(?P<slug>[\w-]+)/?$', object_detail, show_dict, name='show-detail'),
    url(r'^(?P<object_id>\d+)/?$', object_detail, timeslot_dict, name='timeslot-detail'),
    (r'^broadcastformats_box/?$', object_list, broadcastformart_dict,),
    (r'^week/?$', week_schedule)
)
