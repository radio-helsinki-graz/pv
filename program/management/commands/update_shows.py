from django.core.management.base import NoArgsCommand

from program.models import Show


class Command(NoArgsCommand):
    help = 'update shows by setting is_active'

    def handle_noargs(self, **options):
        activated = 0
        deactivated = 0

        for show in Show.objects.exclude(pk=1):
            for programslot in show.programslots.all():
                active_programslots = 0
                if programslot.is_active:
                    active_programslots += 1
                else:
                    active_programslots -= 1

            show.is_active = active_programslots > 0
            show.save()

            if show.is_active:
                activated += 1
            else:
                deactivated += 1

        print "%s shows activated, %s shows de-activated" % (activated, deactivated)
