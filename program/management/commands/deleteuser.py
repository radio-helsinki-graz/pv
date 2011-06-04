from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from optparse import make_option

class Command(BaseCommand):
    help = 'deletes an user'
    option_list = BaseCommand.option_list + (
        make_option('--username', dest='username', default=None, help='Specifies the username.'),
    )

    def handle(self, *args, **options):
        username = options.get('username', None)

        if not username:
            raise CommandError("You must use --username.")
        try:
            User.objects.get(username=username).delete()
        except User.DoesNotExist:
            raise 'user does not exist.'
        else:
            print 'user deleted succesfuly.'