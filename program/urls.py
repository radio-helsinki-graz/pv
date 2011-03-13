from django.conf.urls.defaults import *
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from models import Host, Show, TimeSlot
from views import RecommendationsView, ShowListView

urlpatterns = patterns('',
    ('^hosts/$', ListView.as_view(model=Host, context_object_name='host_list')),
    url('^host/(?P<pk>\d+)/$', DetailView.as_view(model=Host), name='host-detail'),
    ('^recommendations/$', RecommendationsView.as_view()),
    ('^recommendations_box/$', RecommendationsView.as_view(template_name='program/recommendations_box.html')),
    ('^shows/$', ShowListView.as_view()),
    url('^show/(?P<slug>[\w-]+)/$', DetailView.as_view(model=Show), name='show-detail'),
    url('^timeslot/(?P<pk>\d+)/$', DetailView.as_view(model=TimeSlot), name='timeslot-detail'),
)