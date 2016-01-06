from django.core.management.base import NoArgsCommand

from program.models import Host


class Command(NoArgsCommand):
    help = 'update host by setting is_active'

    def handle_noargs(self, **options):
        for host in Host.objects.all():
            for show in host.shows.all():
                hosts_active_show = None
                if show.has_active_programslots:
                    hosts_active_show = True
                else:
                    hosts_active_show = False

                host.hosts_active_show = hosts_active_show

                if not hosts_active_show:
                    host.save()
