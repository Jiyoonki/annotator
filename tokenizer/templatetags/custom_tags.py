from django import template

register = template.Library()

@register.filter(name='orderDict')
def orderDict(value, key):
    """
        Returns the value turned into a list.
    """
    result = value.split(key)
    result = {k: v for k, v in enumerate(result, 1)}

    return result
