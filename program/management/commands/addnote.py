from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError

from datetime import datetime
import sys

from program.models import Show, TimeSlot, Note

class Command(BaseCommand):
    help = 'adds a note to a timeslot'
    args = '<show_id> <date>'
    
    def handle(self, *args, **options):
        if len(args) == 2:
            show_id = args[0]
            start_date = args[1]
        else:
            raise CommandError('you must provide the show_id date')

        try:
            show = Show.objects.get(id=show_id)
        except Show.DoesNotExist as dne:
            raise CommandError(dne)

        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
        except ValueError as ve:
            raise CommandError(ve)
        else:
            year, month, day = start.year, start.month, start.day

        try:
            timeslot = TimeSlot.objects.get(show=show, start__year=year, start__month=month, start__day=day)
        except TimeSlot.DoesNotExist as dne:
            raise CommandError(dne)

        try:
            title = sys.stdin.readline().rstrip()
            lines = sys.stdin.readlines()
        except Exception as e:
            raise CommandError(e)

        owner = show.owners[0] if show.owners.count() > 0 else User.objects.get(pk=1)
        note = Note(timeslot=timeslot, owner=owner, title=title, content=''.join(lines))

        try:
            note.validate_unique()
        except ValidationError as ve:
            raise CommandError(ve.messages[0])
        else:
            note.save()
            print 'added note "%s" to "%s"' % (title, timeslot)
        