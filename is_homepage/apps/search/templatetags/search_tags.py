from django import template

register = template.Library()

@register.simple_tag
def has_matching_terms(terms) -> bool:
    term_counts = sum(terms.values())
    return term_counts > 0