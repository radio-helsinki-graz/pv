from django.conf import settings

import json
import urllib


def get_automation_id_choices():
    base_url = getattr(settings, 'AUTOMATION_BASE_URL', None)
    shows = []
    if base_url:
        shows_list = json.load(urllib.urlopen(base_url))['shows']
        shows = [(s['id'], s['title']) for s in shows_list]
    return shows
