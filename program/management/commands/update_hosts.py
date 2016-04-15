from django.core.management.base import NoArgsCommand

from program.models import Host


class Command(NoArgsCommand):
    help = 'update host by setting is_active'

    def handle_noargs(self, **options):
        activated = 0
        deactivated = 0

        for host in Host.objects.all():
            active_shows = 0
            for show in host.shows.all():
                if show.is_active:
                    active_shows += 1
                else:
                    active_shows -= 1

            host.is_active = active_shows > 0
            host.save()

            if host.is_active:
                activated += 1
            else:
                deactivated += 1

        print "%s hosts activated, %s hosts de-activated " % (activated, deactivated)
