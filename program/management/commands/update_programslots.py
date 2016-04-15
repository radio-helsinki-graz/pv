from django.core.management.base import NoArgsCommand

from program.models import ProgramSlot

from datetime import date


class Command(NoArgsCommand):
    help = 'update programslots by setting is_active'

    def handle_noargs(self, **options):
        activated = 0
        deactivated = 0

        for programslot in ProgramSlot.objects.all():
            programslot.is_active = programslot.until > date.today()
            programslot.save()

            if programslot.is_active:
                activated += 1
            else:
                deactivated += 1

        print "%s program slots activated, %s program slots de-activated" % (activated, deactivated)
