from django import template

register = template.Library()

@register.filter
@register.simple_tag
def update_value(value):
    return value

@register.filter
def get_type(value):
    return type(value)

@register.filter
def index(indexable, i):
    return indexable[int(i)]
    