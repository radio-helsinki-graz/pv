from django import template

from program.models import BroadcastFormat, MusicFocus, ShowInformation, ShowTopic, Language

register = template.Library()


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


@register.inclusion_tag('boxes/language.html')
def language():
    return {'language_list': Language.objects.all()}
