import re
from typing import List
from django.utils.safestring import mark_safe
from django import template

register = template.Library()


@register.filter
def classname(obj):
    return obj.__class__.__name__


@register.filter
def modeltypename(obj):
    match obj.__class__.__name__:
        case 'CaseStudiesDetailPage':
            return 'Case Studies'
        case 'InnovationGuidesIndexPage' | 'InnovationGuidesStagePage' | 'InnovationGuidesDetailPage':
            return 'Innovation guides'
        case 'NewsDetailPage':
            return 'News'
        case 'HelpResourcesIndexPage' | 'HelpResourcesGroupPage' | 'HelpResourcesMenuItemPage' | 'HelpResourcesGenericPage':
            return 'Help and resources'
        case 'Document':
            return 'Documents'
        case _:
            return 'Other'


@register.filter
def highlight(text, search):
    highlighted_text = text
    spitted_search: List[str] = search.split()
    for search_word in spitted_search:
        text = str(highlighted_text)
        src_str = re.compile(r"\b" + search_word + r"\b" , re.IGNORECASE)
        highlighted_text = src_str.sub(f"<span class='highlight'>{search_word}</span>", text)
        
    return mark_safe(highlighted_text)