from django.conf.urls.defaults import *
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from models import Host, Show, TimeSlot
from views import CurrentShowView, DayScheduleView, RecommendationsView, ShowListView, TodayScheduleView

urlpatterns = patterns('',
    ('^$', TodayScheduleView.as_view()),
    ('^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', DayScheduleView.as_view()),
    ('^current/$', CurrentShowView.as_view()),
    ('^hosts/$', ListView.as_view(model=Host, context_object_name='hosts')),
    url('^host/(?P<pk>\d+)/$', DetailView.as_view(model=Host), name='host-detail'),
    ('^recommendations/$', RecommendationsView.as_view()),
    ('^recommendations_box/$', RecommendationsView.as_view(template_name='program/recommendations_box.html')),
    ('^shows/$', ShowListView.as_view()),
    url('^show/(?P<slug>[\w-]+)/$', DetailView.as_view(model=Show), name='show-detail'),
    url('^(?P<pk>\d+)/$', DetailView.as_view(model=TimeSlot), name='timeslot-detail'),
)