from django.conf.urls.defaults import *
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from models import Host, Show, TimeSlot
from views import ShowListView

urlpatterns = patterns('',
    url('^hosts/$', ListView.as_view(model=Host,context_object_name='host_list')),
    url('^host/(?P<pk>\d+)/$', DetailView.as_view(model=Host), name='host-detail'),
    url('^shows/$', ShowListView.as_view(model=Show)),
    url('^show/(?P<slug>[\w-]+)/$', DetailView.as_view(model=Show), name='show-detail'),
    url('^timeslot/(?P<pk>\d+)/$', DetailView.as_view(model=TimeSlot, context_object_name='timeslot'), name='timeslot-detail'),
)