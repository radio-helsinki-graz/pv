from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, ValidationError
from django.core.management.base import NoArgsCommand
from django.utils.html import strip_tags

import MySQLdb

from program.models import Note, Show, TimeSlot

USER = 'helsinki'
PASSWD = 'helsinki'
DB = 'helsinki'


class Command(NoArgsCommand):
    help = 'Import notes from current program'

    def handle_noargs(self, **options):
        connection = MySQLdb.connect(user=USER, passwd=PASSWD, db=DB)
        cursor = connection.cursor()

        cursor.execute("""SELECT n.titel, n.datum, s.titel, n.notiz
FROM notizen AS n JOIN sendungen AS s ON n.sendung_id=s.id
WHERE n.sendung_id in (SELECT id FROM sendungen WHERE letzter_termin > current_date)""")

        counter = 0
        for ntitel, datum, stitel, notiz in cursor.fetchall():
            ntitel = strip_tags(ntitel) if ntitel else strip_tags(stitel)
            stitel = strip_tags(stitel)
            notiz = strip_tags(notiz)

            if stitel.endswith('(Wiederholung)'):
                stitel = stitel[:-15]

            if datum:
                year, month, day = datum.year, datum.month, datum.day
                try:
                    show = Show.objects.get(name=stitel)
                except ObjectDoesNotExist:
                    print 'show with name "%s" not found' % stitel
                else:
                    try:
                        timeslot = TimeSlot.objects.get(programslot__show=show, start__year=year, start__month=month,
                                                        start__day=day)
                    except ObjectDoesNotExist:
                        print 'no timeslot found for sendung "%s" and datum "%s"' % (stitel, datum)
                    except MultipleObjectsReturned:
                        print 'multiple timeslots found for sendung "%s" and datum "%s"' % (stitel, datum)
                    else:
                        note = Note(timeslot=timeslot, title=ntitel, content=notiz)
                        try:
                            note.validate_unique()
                        except ValidationError:
                            print 'note already imported for show "%s" and datum "%s"' % (stitel, datum)
                        else:
                            try:
                                note.save()
                            except:
                                print 'could not save note "%s" for show "%s" and datum "%s"' % (ntitel, stitel, datum)
                            else:
                                counter += 1

        cursor.close()
        connection.close()

        print '%i notes imported' % counter
