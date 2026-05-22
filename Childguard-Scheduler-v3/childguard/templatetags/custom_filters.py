from django import template

register = template.Library()


@register.filter
def split(value, separator=','):
    """Splits een string op een scheidingsteken. Gebruik: "a,b,c"|split:"," """
    return value.split(separator)
