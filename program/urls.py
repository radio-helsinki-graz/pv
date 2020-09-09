import os

from django.conf import settings
from django.conf.urls import url
from django.views.decorators.cache import cache_page
from django.views.static import serve

from .views import DayScheduleView, WeekScheduleView, CurrentShowBoxView, HostListView, HostDetailView, RecommendationsListView, \
    RecommendationsBoxView, ShowListView, ShowDetailView, TimeSlotDetailView, StylesView

PROGRAM_SITE_MEDIA = os.path.join(os.path.dirname(__file__), '../site_media')

urlpatterns = [
    url(r'^today/?$', DayScheduleView.as_view()),
    url(r'^week/?$', WeekScheduleView.as_view()),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/?$', DayScheduleView.as_view()),
    url(r'^(?P<year>\d{4})/(?P<week>\d{1,2})/?$', WeekScheduleView.as_view()),
    url(r'^current_box/?$', cache_page(60)(CurrentShowBoxView.as_view())),
    url(r'^hosts/?$', HostListView.as_view()),
    url(r'^hosts/(?P<pk>\d+)/?$', HostDetailView.as_view(), name='host-detail'),
    url(r'^tips/?$', RecommendationsListView.as_view()),
    url(r'^tips_box/?$', RecommendationsBoxView.as_view()),
    url(r'^shows/?$', ShowListView.as_view()),
    url(r'^shows/(?P<slug>[\w-]+)/?$', ShowDetailView.as_view(), name='show-detail'),
    url(r'^(?P<pk>\d+)/?$', TimeSlotDetailView.as_view(), name='timeslot-detail'),
    url(r'^styles.css$', StylesView.as_view())
]

if settings.DEBUG:
    urlpatterns.append(url(r'^static/(?P<path>.*)$', serve, {'document_root': PROGRAM_SITE_MEDIA}))
