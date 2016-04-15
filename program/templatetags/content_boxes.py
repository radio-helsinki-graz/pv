# http://docs.djangoproject.com/en/1.2/howto/custom-template-tags/

from django import template
register = template.Library()

from program.models import BroadcastFormat, MusicFocus, ShowInformation, ShowTopic


@register.inclusion_tag('boxes/broadcastformat.html')
def broadcastformat():
    return {'broadcastformat_list': BroadcastFormat.objects.filter(enabled=True)}


@register.inclusion_tag('boxes/musicfocus.html')
def musicfocus():
    return {'musicfocus_list': MusicFocus.objects.all()}


@register.inclusion_tag('boxes/showinformation.html')
def showinformation():
    return {'showinformation_list': ShowInformation.objects.all()}


@register.inclusion_tag('boxes/showtopic.html')
def showtopic():
    return {'showtopic_list': ShowTopic.objects.all()}
