from django.core.management.base import NoArgsCommand

from program.models import Show

from datetime import date


class Command(NoArgsCommand):
    help = 'update shows by setting is_active'

    def handle_noargs(self, **options):
        for show in Show.objects.exclude(pk=1):
            is_active = None
            for programslot in show.programslots.all():
                if programslot.until > date.today():
                    is_active = True
                else:
                    is_active = False
            show.is_active = is_active

            if not is_active:
                show.save()
