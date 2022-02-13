from django import template
register = template.Library()


@register.filter(name='censor')
def censor(value):
    censor_list = ['слово1', 'слово2']
    for a in censor_list:
        while True:
            if a in value:
                value = value.replace(a, 'CENSOR')
            else:
                break
    return value
