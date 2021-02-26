from django import template

from program.models import BroadcastFormat, MusicFocus, ShowInformation, ShowTopic, Language

register = template.Library()


@register.inclusion_tag('v2/filters/broadcastformat.html')
def broadcastformatV2():
    return {'broadcastformat_list': BroadcastFormat.objects.filter(enabled=True)}


@register.inclusion_tag('v2/filters/musicfocus.html')
def musicfocusV2():
    return {'musicfocus_list': MusicFocus.objects.all()}


@register.inclusion_tag('v2/filters/showinformation.html')
def showinformationV2():
    return {'showinformation_list': ShowInformation.objects.all()}


@register.inclusion_tag('v2/filters/showtopic.html')
def showtopicV2():
    return {'showtopic_list': ShowTopic.objects.all()}


@register.inclusion_tag('v2/filters/language.html')
def languageV2():
    return {'language_list': Language.objects.all()}
