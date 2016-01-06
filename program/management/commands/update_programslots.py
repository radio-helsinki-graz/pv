from django.core.management.base import NoArgsCommand

from program.models import ProgramSlot

from datetime import date


class Command(NoArgsCommand):
    help = 'update programslots by setting is_active'

    def handle_noargs(self, **options):
        for programslot in ProgramSlot.objects.all():
            programslot.is_active = programslot.until > date.today()
            programslot.save()
