from django.core.management.base import NoArgsCommand

from program.models import Host


class Command(NoArgsCommand):
    help = 'update host by setting is_active'

    def handle_noargs(self, **options):
        for host in Host.objects.all():
            for show in host.shows.all():
                is_active = None
                if show.is_active:
                    is_active = True
                else:
                    is_active = False

                host.is_active = is_active

                if not is_active:
                    host.save()
