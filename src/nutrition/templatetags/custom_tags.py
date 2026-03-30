from django import template

register = template.Library()

@register.filter(name='verbose_name')
def verbose_name(obj, field_name):
    return obj._meta.get_field(field_name).verbose_name
