# -*- coding: utf-8 -*-

import codecs
import sys
from datetime import date, datetime, time, timedelta
from django.core.management.base import BaseCommand, CommandError
from program.models import TimeSlot


class Command(BaseCommand):
    help = 'export playlog for one year'
    args = '<year>'

    def handle(self, *args, **options):
        UTF8Writer = codecs.getwriter('utf8')
        sys.stdout = UTF8Writer(sys.stdout)

        if len(args) == 1:
            try:
                year = int(args[0])
            except ValueError:
                raise CommandError("'%s' is not a valid year" % args[0])
        else:
            raise CommandError('you must provide the year')

        print "# Radio Helsinki Sendungslog %d" % year

        start = datetime.strptime('%d__01__01__00__00' % (year), '%Y__%m__%d__%H__%M')
        end = datetime.strptime('%d__01__01__00__00' % (year+1), '%Y__%m__%d__%H__%M')

        currentDate = None
        for ts in TimeSlot.objects.filter(end__gt=start, start__lt=end).select_related('programslot').select_related('show'):
            if currentDate == None or currentDate < ts.start.date():
                if currentDate:
                    print "\n"
                currentDate = ts.start.date()
                print currentDate.strftime("## %a %d.%m.%Y:\n")

            title = ts.show.name
            if ts.programslot.is_repetition:
                title += " (WH)"

            print " * **%s - %s**: %s" % (ts.start.strftime("%H:%M:%S"), ts.end.strftime("%H:%M:%S"), title)

