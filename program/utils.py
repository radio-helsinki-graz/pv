from django.conf import settings

import json
import urllib

def get_automation_id_choices():
    shows_list = json.load(urllib.urlopen(settings.AUTOMATION_BASE_URL))['shows']
    shows = [(s['id'], s['title']) for s in shows_list]
    return shows