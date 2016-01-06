from django.conf import settings
from django.conf.urls import patterns, url
from django.views.decorators.cache import cache_page

import views

import os

PROGRAM_SITE_MEDIA = os.path.join(os.path.dirname(__file__), '../site_media')


urlpatterns = patterns('',
                       url(r'^today/?$', views.DayScheduleView.as_view()),
                       url(r'^week/?$', views.WeekScheduleView.as_view()),
                       url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/?$', views.DayScheduleView.as_view()),
                       url(r'^(?P<year>\d{4})/(?P<week>\d{1,2})/?$', views.WeekScheduleView.as_view()),
                       url(r'^current_box/?$', cache_page(60)(views.CurrentShowBoxView.as_view())),
                       url(r'^hosts/?$', views.HostListView.as_view()),
                       url(r'^hosts/(?P<pk>\d+)/?$', views.HostDetailView.as_view(), name='host-detail'),
                       url(r'^tips/?$', views.RecommendationsListView.as_view()),
                       url(r'^tips_box/?$', views.RecommendationsBoxView.as_view()),
                       url(r'^shows/?$', views.ShowListView.as_view()),
                       url(r'^shows/(?P<slug>[\w-]+)/?$', views.ShowDetailView.as_view(), name='show-detail'),
                       url(r'^(?P<pk>\d+)/?$', views.TimeSlotDetailView.as_view(), name='timeslot-detail'),
                       url(r'^styles.css$', views.StylesView.as_view())
                       )
if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': PROGRAM_SITE_MEDIA}))
