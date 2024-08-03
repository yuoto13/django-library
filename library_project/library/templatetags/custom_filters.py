import datetime
from django import template

register = template.Library()

@register.filter
def time_since_days(value):
    if not isinstance(value, datetime.datetime):
        return value
    today = datetime.datetime.now().astimezone(value.tzinfo) if value.tzinfo else datetime.datetime.now()
    delta = today - value
    return delta.days
