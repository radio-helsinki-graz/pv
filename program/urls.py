from django.conf import settings
from django.conf.urls import patterns, url
from django.views.decorators.cache import cache_page

from views import current_show, day_schedule, recommendations, show_list, show_detail, timeslot_detail, week_schedule, styles, host_list, host_detail

import os

PROGRAM_SITE_MEDIA = os.path.join(os.path.dirname(__file__), '../site_media')

recommendations_dict = {'template_name': 'boxes/recommendations.html'}

urlpatterns = patterns('',
                       url(r'^today/?$', day_schedule),
                       url(r'^week/?$', week_schedule),
                       url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/?$', day_schedule),
                       url(r'^(?P<year>\d{4})/(?P<week>\d{1,2})/?$', week_schedule),
                       url(r'^current_box/?$', cache_page(60)(current_show)),
                       url(r'^hosts/?$', host_list),
                       url(r'^hosts/(?P<object_id>\d+)/?$', host_detail, name='host-detail'),
                       url(r'^tips/?$', recommendations),
                       url(r'^tips_box/?$', recommendations, recommendations_dict),
                       url(r'^shows/?$', show_list),
                       url(r'^shows/(?P<slug>[\w-]+)/?$', show_detail, name='show-detail'),
                       url(r'^(?P<object_id>\d+)/?$', timeslot_detail, name='timeslot-detail'),
                       url(r'^styles.css$', styles))

if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': PROGRAM_SITE_MEDIA}))
