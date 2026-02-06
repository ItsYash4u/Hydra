from django import template

register = template.Library()


@register.filter
def get_item(obj, key):
    """
    Safely get a key from a dict-like object.
    Usage: {{ my_dict|get_item:"key" }}
    """
    if isinstance(obj, dict):
        return obj.get(key, "")
    return ""
