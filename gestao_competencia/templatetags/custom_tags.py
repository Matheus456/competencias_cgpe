from django import template

register = template.Library()

@register.simple_tag
def update_value(value):
    return value
    
register.filter('update_value', update_value)