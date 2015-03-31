from django import template
from django.template.defaultfilters import stringfilter

import re

register = template.Library()

@register.filter
@stringfilter
def strip_time(value, include_ago=True):
    """
    Filter: removes hours from a timesince output

    Example:

    {{ created_datetime|timesince|strip_time }}
    """

    value = re.sub(r'(, )?\d+\s+(hours?|minutes?)', '', value).strip()
    if value == "":
        value = "today"
    else:
        if include_ago:
            value = "{} ago".format(value)

    return value
