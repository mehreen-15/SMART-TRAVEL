from django import template
import re

register = template.Library()

@register.filter
def split(value, delimiter=','):
    """
    Split a string by the specified delimiter.
    Example: {{ value|split:"," }}
    """
    if value:
        return [item.strip() for item in value.split(delimiter)]
    return []

@register.filter
def get_item(dictionary, key):
    """
    Get an item from a dictionary by key.
    
    Example:
        {{ my_dict|get_item:key_variable }}
    """
    return dictionary.get(key)

@register.filter
def stars(value):
    """
    Convert a numeric rating to stars display.
    
    Example:
        {{ 4.5|stars }}
        Returns: ★★★★½
    """
    full_stars = int(value)
    half_star = (value - full_stars) >= 0.5
    
    result = '★' * full_stars
    if half_star:
        result += '½'
    
    return result 