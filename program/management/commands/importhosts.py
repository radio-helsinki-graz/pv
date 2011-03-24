from django.core.management.base import NoArgsCommand

import MySQLdb

from helsinki.program.models import Host

USER = 'helsinki'
PASSWD = 'helsinki'
DB = 'helsinki'

class Command(NoArgsCommand):
    help = 'Import hosts from current program'

    def handle_noargs(self, **options):
        connection = MySQLdb.connect(user=USER, passwd=PASSWD, db=DB)
        cursor = connection.cursor()

        cursor.execute("""SELECT DISTINCT macher
FROM sendungen
WHERE letzter_termin > current_date AND macher != '' AND titel NOT LIKE 'Musikprogramm'""")

        counter = 0

        for row in cursor.fetchall():
            for macher in row[0].decode('latin1').encode('utf8').split(','):
                host = Host(name=macher.strip())
                host.save()

                counter += 1

        cursor.close()
        connection.close()

        print '%i hosts imported' % counter
