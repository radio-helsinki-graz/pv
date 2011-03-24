from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.management.base import NoArgsCommand
from django.template.defaultfilters import slugify
from django.utils.html import clean_html, strip_tags

import MySQLdb

from helsinki.program.models import BroadcastFormat, Host, Show

USER = 'helsinki'
PASSWD = 'helsinki'
DB = 'helsinki'

TALK = BroadcastFormat.objects.get(pk=1)

class Command(NoArgsCommand):
    help = 'Import shows from the current program'
    
    def handle_noargs(self, **options):
        connection = MySQLdb.connect(user=USER, passwd=PASSWD, db=DB)
        cursor = connection.cursor()

        cursor.execute("""SELECT titel, beschreibung, web, macher
FROM sendungen
WHERE letzter_termin > current_date AND titel NOT LIKE 'Musikprogramm' AND titel NOT LIKE '%%(Wiederholung)'
ORDER BY titel, beginn, ende""")

        counter = 0

        for titel, beschreibung, web, macher in cursor.fetchall():
            titel = strip_tags(titel.decode('latin1').encode('utf8'))
            beschreibung = clean_html(beschreibung.decode('latin1').encode('utf8'))

            slug = slugify(titel)

            hosts = []

            for macher in macher.decode('latin1').encode('utf8').split(','):
                macher = macher.strip()
                try:
                    host = Host.objects.get(name=macher)
                except MultipleObjectsReturned:
                    print 'multiple hosts with name "%s" found' % macher
                except ObjectDoesNotExist:
                    print 'host with name "%s" not found' % macher
                else:
                    hosts.append(host)

            try:
                show = Show.objects.get(name=titel)
                print 'sendung "%s" already imported as show "%s"' % (titel, show)
            except ObjectDoesNotExist:
                show = Show(broadcastformat=TALK, name=titel, slug=slug, short_description='FIXME', description=beschreibung)
                try:
                    show.save()
                    counter += 1
                except:
                    print 'sendung "%s" could not be imported' % titel
                else:
                    for h in hosts:
                        show.hosts.add(h)
                        show.save()

        cursor.close()
        connection.close()

        print '%i shows imported' % counter
