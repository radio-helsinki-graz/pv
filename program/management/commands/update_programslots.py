from django.core.management.base import NoArgsCommand

from program.models import ProgramSlot

from datetime import datetime


class Command(NoArgsCommand):
    help = 'update programslots by setting is_active'

    def handle_noargs(self, **options):
        deactivated = ProgramSlot.objects.filter(until__lt=datetime.now()).update(is_active=False)
        activated = ProgramSlot.objects.filter(until__gt=datetime.now()).update(is_active=True)

        print "%s program slots activated, %s program slots de-activated" % (activated, deactivated)
