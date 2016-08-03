from django.core.management.base import BaseCommand, CommandError

from program.models import ProgramSlot


class Command(BaseCommand):
    help = 'removes the automation_id from the program slots'
    args = '<automation_id>'

    def handle(self, *args, **options):
        if len(args) == 1:
            automation_id = args[0]
        else:
            raise CommandError('you must provide the automation_id')

        ProgramSlot.objects.filter(automation_id=automation_id).update(automation_id=None)
