from django import template

from ..models import MenuSnippet

register = template.Library()


@register.simple_tag()
def get_menu(slug):
    return MenuSnippet.objects.filter(slug=slug).first()
