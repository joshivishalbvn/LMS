from django import template
from django.forms import widgets

register = template.Library()

@register.filter
def is_checkbox(widget):
    """Check if the widget is an instance of CheckboxInput."""
    return isinstance(widget, widgets.CheckboxInput)
