from django import template

register = template.Library()

@register
def sub(value, arg):
    return value - arg