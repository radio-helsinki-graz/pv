from django import template

register = template.Library()

from datetime import datetime, time, timedelta

@register.simple_tag
def duration(start, end):
    return 'style="height: %dpx"' % ((end-start).seconds/60)

@register.simple_tag
def duration_until(end):
    start = datetime.combine(end.date(), time(6,0))
    return 'style="height: %dpx"' % ((end-start).seconds/60)

@register.simple_tag
def duration_since(start):
    if start.time() < time(23,59):
        end = datetime.combine(start.date()+timedelta(days=1), time(6,0))
    else:
        end = datetime.combine(start.date(), time(6,0))
    return 'style="height: %dpx"' % ((end-start).seconds/60)