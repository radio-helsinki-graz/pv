from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import NoArgsCommand
from django.utils.html import strip_tags

from datetime import time
import MySQLdb

from helsinki.program.models import Show, ProgramSlot, RRule

USER = 'helsinki'
PASSWD = 'helsinki'
DB = 'helsinki'

RRULES = {
    0: RRule.objects.get(pk=1),
    7: RRule.objects.get(pk=3),
    14: RRule.objects.get(pk=4),
    28: RRule.objects.get(pk=5)
}

class Command(NoArgsCommand):
    help = 'Import programslots from the current program'

    def handle_noargs(self, **options):
        connection = MySQLdb.connect(user=USER, passwd=PASSWD, db=DB)
        cursor = connection.cursor()

        cursor.execute("""SELECT titel, beginn, ende, erster_termin, letzter_termin, rhytmus, termin
FROM sendungen
WHERE letzter_termin > current_date AND titel NOT LIKE 'Musikprogramm' AND titel NOT LIKE '%%(Wiederholung)'""")

        counter = 0

        for titel, beginn, ende, erster_termin, letzter_termin, rhytmus, termin in cursor.fetchall():
            titel = strip_tags(titel.decode('latin1').encode('utf8'))

            hours, seconds = divmod(beginn.seconds, 3600)
            minutes, seconds = divmod(seconds, 60)
            tstart = time(hour=hours, minute=minutes, second=seconds)

            hours, seconds = divmod(ende.seconds, 3600)
            minutes, seconds = divmod(seconds, 60)
            tend = time(hour=hours, minute=minutes, second=seconds)

            try:
                rrule = RRULES[rhytmus]
                try:
                    show = Show.objects.get(name=titel)
                except ObjectDoesNotExist:
                    print 'show with name "%s" not found' % titel
                else:
                    programslot = ProgramSlot(rrule=rrule, byweekday=termin, show=show, dstart=erster_termin, tstart=tstart,
                                              tend=tend, until=letzter_termin)
                    try:
                        programslot.save()
                        counter += 1
                    except:
                        pass
            except KeyError:
                print 'rhythmus "%i" is not supported for sendung "%s"' % (rhytmus, titel)

        cursor.execute("""SELECT titel, beginn, ende, erster_termin, letzter_termin, rhytmus, termin
FROM sendungen
WHERE letzter_termin > current_date AND titel LIKE '%%(Wiederholung)'""")

        for titel, beginn, ende, erster_termin, letzter_termin, rhytmus, termin in cursor.fetchall():
            titel = titel.decode('latin1').encode('utf8')[:-15]

            hours, seconds = divmod(beginn.seconds, 3600)
            minutes, seconds = divmod(seconds, 60)
            tstart = time(hour=hours, minute=minutes, second=seconds)

            hours, seconds = divmod(ende.seconds, 3600)
            minutes, seconds = divmod(seconds, 60)
            tend = time(hour=hours, minute=minutes, second=seconds)

            try:
                rrule = RRULES[rhytmus]
                try:
                    show = Show.objects.get(name=titel)
                except ObjectDoesNotExist:
                    print 'show with name "%s" not found' % titel
                else:
                    programslot = ProgramSlot(rrule=rrule, byweekday=termin, show=show, dstart=erster_termin, tstart=tstart, tend=tend, until=letzter_termin, is_repetition=True)
                    try:
                        programslot.save()
                        counter += 1
                    except:
                        pass
            except KeyError:
                print 'rhythmus "%i" is not supported for sendung "%s"' % (rhytmus, titel)

        cursor.close()
        connection.close()

        print '%i programslots imported' % counter
