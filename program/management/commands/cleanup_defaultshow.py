from django.core.management.base import NoArgsCommand
from django.db import transaction

from program.models import Show, TimeSlot, ProgramSlot

class Command(NoArgsCommand):
    @transaction.commit_manually
    def handle_noargs(self, **options):
        help = 'removes default shows without note'

        default_show = Show.objects.get(pk=1)
        try:
            TimeSlot.objects.filter(show=default_show, note__isnull=True).delete()
            for programslot in ProgramSlot.objects.filter(show=default_show):
                if programslot.timeslots.count() == 0:
                    programslot.delete()
        except:
            transaction.rollback()
        else:
            transaction.commit()

