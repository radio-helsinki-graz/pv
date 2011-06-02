from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from optparse import make_option

class Command(BaseCommand):
    help = 'creates an user'
    option_list = BaseCommand.option_list + (
        make_option('--username', dest='username', default=None, help='Specifies the username.'),
        make_option('--email', dest='email', default=None, help='Specifies the email address.'),
    )

    def handle(self, *args, **options):
        username = options.get('username', None)
        email = options.get('email', None)

        if not username or not email:
            raise CommandError("You must use --username and --email.")
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            User.objects.create_user(username=username, email=email)
            print 'user created successfully.'
        else:
            print 'User already exists, no need to create.'
