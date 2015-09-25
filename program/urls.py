from django.conf import settings
from django.conf.urls import patterns, url, include
from django.db.models import Q
from django.views.decorators.cache import cache_page
from django.views.generic.detail import DetailView

from models import Host, Show, TimeSlot
from views import current_show, day_schedule, recommendations, show_list, \
    week_schedule, styles

from datetime import date

hosts_dict = {
    'queryset': Host.objects.filter(
        Q(shows__programslots__until__gte=date.today()) |
        Q(always_visible=True)).distinct(),
    'template_object_name': 'host'
}
shows_dict = {
    'queryset': Show.objects.filter(
        programslots__until__gt=date.today()).exclude(id=1).distinct(),
    'template_object_name': 'show'
}
timeslots_dict = {
    'queryset': TimeSlot.objects.all(),
    'template_object_name': 'timeslot'
}
recommendations_dict = {'template_name': 'boxes/recommendations.html'}

urlpatterns = patterns('',
                       url(r'^today/?$', day_schedule),
                       url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/?$',
                           day_schedule),
                       url(r'^(?P<year>\d{4})/(?P<week>\d{1,2})/?$',
                           week_schedule),
                       url(r'^current_box/?$', cache_page(60)(current_show)),
                       url(r'^hosts/?$',
                           DetailView,
                           dict(hosts_dict, template_name='host_list.html')),
                       url(r'^hosts/(?P<object_id>\d+)/?$', DetailView,
                           dict(hosts_dict, template_name='host_detail.html'),
                           name='host-detail'),
                       url(r'^tips/?$', recommendations),
                       url(r'^tips_box/?$', recommendations,
                           recommendations_dict),
                       url(r'^shows/?$', show_list),
                       url(r'^shows/(?P<slug>[\w-]+)/?$', DetailView,
                           dict(shows_dict, template_name='show_detail.html'),
                           name='show-detail'),
                       url(r'^(?P<object_id>\d+)/?$', DetailView,
                           dict(timeslots_dict,
                                template_name='timeslot_detail.html'),
                           name='timeslot-detail'),
                       url(r'^week/?$', week_schedule),
                       url(r'^styles.css$', styles))

if settings.DEBUG:
    import os

    PROGRAM_STATIC_DIR = os.path.join(os.path.dirname(__file__),
                                      '../site_media')
    urlpatterns += patterns('',
                            url(r'^static/(?P<path>.*)$',
                                'django.views.static.serve',
                                {'document_root': PROGRAM_STATIC_DIR}))
