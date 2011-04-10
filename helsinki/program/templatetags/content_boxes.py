# http://docs.djangoproject.com/en/dev/howto/custom-template-tags/

from django import template
register = template.Library()

from helsinki.program.models import (
        BroadcastFormat,
        MusicFocus,
        ShowInformation,
        ShowTopic)

@register.inclusion_tag('program/box_broadcastformats.html')
def broadcastformats():
    broadcastformats = BroadcastFormat.objects.all()
    return {'broadcastformats': broadcastformats}
