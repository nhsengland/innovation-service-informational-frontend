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
