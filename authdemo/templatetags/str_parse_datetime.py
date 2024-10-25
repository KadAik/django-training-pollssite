
from django import template
from datetime import datetime


register = template.Library()


@register.filter
def str_parse_datetime(value, fmt="%Y-%m-%d %H:%M:%S.%f%z"):
    """ Parse a string datetime to datetime object """
    return datetime.strptime(value, fmt)



