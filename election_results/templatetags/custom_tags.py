from datetime import datetime
from django import template
register = template.Library()

@register.filter
def attr_sort(objects, attr):
    """
    Sorts `objects` by `attr` (ascending).
    (Currently unused; just an example.)

    Args:
        objects (iterable of object):
            List of objects
        attr (str):
            Attribute name of objects to sort by.

    Returns:
        list of object:
            Sorted `objects` as a list.
    """
    return sorted(objects, key=lambda o: getattr(o, attr, None))

@register.simple_tag
def current_time(fmt="%H:%M:%S"):
    """
    Args:
        fmt (str, optional):
            Format string.
            Default: "%H:%M:%S"

    Returns:
        str:
            Time as a string.
    """
    return datetime.now().strftime(fmt)
