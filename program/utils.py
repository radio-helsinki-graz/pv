from django.conf import settings

import json
import urllib
from os.path import join
from datetime import datetime, date, timedelta


def get_automation_id_choices():
    base_url = getattr(settings, 'AUTOMATION_BASE_URL', None)
    cache_dir = getattr(settings, 'AUTOMATION_CACHE_DIR', 'cache')
    cached_shows = join(cache_dir, 'shows.json')
    shows = []
    if base_url:
        try:
            shows_json = urllib.urlopen(base_url).read()
            shows_list = json.loads(shows_json)['shows']
        except IOError:
            try:
                with open(cached_shows) as cache:
                    shows_list = json.loads(cache.read())['shows']
            except IOError:
                shows_list = []
        else:
            with open(cached_shows, 'w') as cache:
                cache.write(shows_json)

        shows = [(s['id'], '%d | %s' % (s['id'], s['title'])) for s in shows_list]
    return shows


def tofirstdayinisoweek(year, week):
    # http://stackoverflow.com/questions/5882405/get-date-from-iso-week-number-in-python
    ret = datetime.strptime('%04d-%02d-1' % (year, week), '%Y-%W-%w')
    if date(year, 1, 4).isoweekday() > 4:
        ret -= timedelta(days=7)
    return ret
