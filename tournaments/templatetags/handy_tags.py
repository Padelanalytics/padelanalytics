from django import template


register = template.Library()


@register.filter(name="jsdate")
def jsdate(d):
    """Formats a python date in a js Date() constructor"""
    try:
        # return "new Date({0},{1},{2})".format(d.year, d.month - 1, d.day)
        # return "({0},{1},{2})".format(d.year, d.month - 1, d.day)
        return d.isoformat()

    except AttributeError:
        return "undefined"
