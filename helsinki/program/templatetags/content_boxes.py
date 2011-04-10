# http://docs.djangoproject.com/en/dev/howto/custom-template-tags/

from django import template
register = template.Library()

from helsinki.program.models import (
        BroadcastFormat,
        MusicFocus,
        ShowInformation,
        ShowTopic)

@register.inclusion_tag('program/box_broadcastformat.html')
def broadcastformat():
    broadcastformats = BroadcastFormat.objects.all()
    return {'broadcastformats': broadcastformats}

@register.inclusion_tag('program/box_musicfocus.html')
def musicfocus():
    musicfoci = MusicFocus.objects.all()
    return {'musicfoci': musicfoci}

@register.inclusion_tag('program/box_showinformation.html')
def showinformation():
    showinformations = ShowInformation.objects.all()
    return {'showinformations': showinformations}

@register.inclusion_tag('program/box_showtopic.html')
def showtopic():
    showtopics = ShowTopic.objects.all()
    return {'showtopics': showtopics}
