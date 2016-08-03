import json
from os.path import join

from django.conf import settings
from django.core.management.base import NoArgsCommand

from program.models import ProgramSlot


class Command(NoArgsCommand):
    help = 'checks the automation_ids used by program slots against the exported'

    def handle_noargs(self, **options):
        cache_dir = getattr(settings, 'AUTOMATION_CACHE_DIR', 'cache')
        cached_shows = join(cache_dir, 'shows.json')
        with open(cached_shows) as shows_json:
            shows = json.loads(shows_json.read())['shows']

            automation_ids = []
            for show in shows:
                automation_ids.append(show['id'])
            automation_ids.sort()

            automation_ids2 = []
            for programslot in ProgramSlot.objects.filter(automation_id__isnull=False):
                automation_ids2.append(int(programslot.automation_id))
            automation_ids2.sort()

            for automation_id in automation_ids:
                if automation_id not in automation_ids2:
                    print '+', automation_id

            for automation_id in automation_ids2:
                if automation_id not in automation_ids:
                    print '-', automation_id
