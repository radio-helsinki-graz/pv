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
            shows = json.loads(shows_json.read())

            rd_ids = {}
            for show in shows['shows']:
                rd_ids[show['id']] = show
            for show in shows['multi-shows']:
                rd_ids[show['id']] = show

            pv_ids = []
            for programslot in ProgramSlot.objects.filter(automation_id__isnull=False):
                pv_ids.append(int(programslot.automation_id))

            for automation_id in sorted(rd_ids.iterkeys()):
                if rd_ids[automation_id]['type'] == 's':
                    continue

                multi_id = -1
                if 'multi' in rd_ids[automation_id]:
                    multi_id = rd_ids[automation_id]['multi']['id']
                if automation_id not in pv_ids and multi_id not in pv_ids:
                    if multi_id < 0:
                        print '+ %d' % (automation_id)
                    else:
                        print '+ %d (%d)' % (automation_id, multi_id)

            for automation_id in sorted(pv_ids):
                if automation_id not in rd_ids:
                    print '-', automation_id
