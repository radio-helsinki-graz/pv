from django.core.management.base import NoArgsCommand

from program.models import Show

from datetime import date


class Command(NoArgsCommand):
    help = 'update shows by setting is_active'

    def handle_noargs(self, **options):
        for show in Show.objects.exclude(pk=1):
            has_active_programslots = None
            for programslot in show.programslots.all():
                if programslot.until > date.today():
                    has_active_programslots = True
                else:
                    has_active_programslots = False
            show.has_active_programslots = has_active_programslots

            if not has_active_programslots:
                show.save()
