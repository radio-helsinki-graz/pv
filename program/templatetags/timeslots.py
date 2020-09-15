from django import template

from datetime import datetime, time, timedelta

register = template.Library()


@register.simple_tag
def height(start, end):
    if start.year == 2020 and int(start.strftime('%V')) >= 5 and start.hour == 12 and start.minute == 0:
        if end.minute == 5:
            return '30'
        return '%d' % (((end - start).seconds / 60) + 25)
    else:
        return '%d' % ((end - start).seconds / 60)


@register.simple_tag
def height_until(end):
    start = datetime.combine(end.date(), time(6, 0))
    return '%d' % ((end - start).seconds / 60)


@register.simple_tag
def height_since(start):
    if start.time() < time(23, 59):
        end = datetime.combine(start.date() + timedelta(days=1), time(6, 0))
    else:
        end = datetime.combine(start.date(), time(6, 0))
    return '%d' % ((end - start).seconds / 60)
