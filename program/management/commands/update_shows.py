from django.core.management.base import NoArgsCommand

from program.models import Show

from datetime import datetime


class Command(NoArgsCommand):
    help = 'update shows by setting is_active'

    def handle_noargs(self, **options):
        deactivated = Show.objects.exclude(id=1).filter(programslots__until__lt=datetime.now()).update(is_active=False)
        activated = Show.objects.exclude(id=1).filter(programslots__until__gt=datetime.now()).distinct().update(is_active=True)

        print "%s shows activated, %s shows de-activated" % (activated, deactivated)
