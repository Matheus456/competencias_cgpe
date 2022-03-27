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
    
@register.filter
def return_scale(skill_obj):
    if skill_obj.escala:
        scale = skill_obj.escala
        return [scale.legenda_1, scale.legenda_2, scale.legenda_3, scale.legenda_4, scale.legenda_5]
    else:
        return ["Nenhuma Experiência", "", "Alguma Experiência", "", "Bastante Experiência"]