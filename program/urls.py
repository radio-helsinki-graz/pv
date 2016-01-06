from django.conf import settings
from django.conf.urls import patterns, url
from django.db.models import Q
from django.views.decorators.cache import cache_page
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from views import ShowListView, CurrentShowBoxView, RecommendationsListView, RecommendationsBoxView, DayScheduleView, StylesView, WeekScheduleView
from models import Host, Show, TimeSlot

import os
from datetime import date, datetime, timedelta

PROGRAM_SITE_MEDIA = os.path.join(os.path.dirname(__file__), '../site_media')

now = datetime.now()
end = now + timedelta(weeks=1)

hosts = Host.objects.filter(Q(shows__programslots__until__gte=date.today()) |
                            Q(always_visible=True)).distinct()
shows = Show.objects.filter(programslots__until__gt=date.today()).exclude(id=1).distinct()
timeslots = TimeSlot.objects.all()
recommendations = TimeSlot.objects.filter(Q(note__isnull=False, note__status=1, start__range=(now, end)) |
                                          Q(show__broadcastformat__slug='sondersendung', start__range=(now, end))).order_by('start')[:20]

urlpatterns = patterns('',
                       url(r'^today/?$', DayScheduleView.as_view()),
                       url(r'^week/?$', WeekScheduleView.as_view()),
                       url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/?$', DayScheduleView.as_view()),
                       url(r'^(?P<year>\d{4})/(?P<week>\d{1,2})/?$', WeekScheduleView.as_view()),
                       url(r'^current_box/?$', cache_page(60)(CurrentShowBoxView.as_view())),
                       url(r'^hosts/?$', ListView.as_view(context_object_name='host_list', queryset=hosts, template_name='host_list.html')),
                       url(r'^hosts/(?P<pk>\d+)/?$', DetailView.as_view(context_object_name='host', queryset=hosts, template_name='host_detail.html'), name='host-detail'),
                       url(r'^tips/?$', RecommendationsListView.as_view()),
                       url(r'^tips_box/?$', RecommendationsBoxView.as_view()),
                       url(r'^shows/?$', ShowListView.as_view(context_object_name='show_list', queryset=shows, template_name='show_list.html')),
                       url(r'^shows/(?P<slug>[\w-]+)/?$', DetailView.as_view(queryset=shows, template_name='show_detail.html'), name='show-detail'),
                       url(r'^(?P<pk>\d+)/?$', DetailView.as_view(queryset=timeslots, template_name='timeslot_detail.html'), name='timeslot-detail'),
                       url(r'^styles.css$', StylesView.as_view())
                       )
if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': PROGRAM_SITE_MEDIA}))
