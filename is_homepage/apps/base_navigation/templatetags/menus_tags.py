from django import template

from ..models import BaseNavigationSnippet

register = template.Library()


@register.simple_tag()
def get_navigation_menu(slug):
    return BaseNavigationSnippet.objects.filter(slug=slug).first()
