from django import template

register = template.Library()


@register.filter
def classname(obj):
    return obj.__class__.__name__


@register.filter
def pagetypename(obj):
    match obj.__class__.__name__:
        case 'CaseStudiesDetailPage':
            return 'Case Studies'
        case 'GenericPage' | 'GenericNavigationIndexPage' | 'GenericNavigationDetailPage':
            return 'Other'
        case 'InnovationGuidesStagePage' | 'InnovationGuidesDetailPage':
            return 'Innovation guides'
        case 'NewsDetailPage':
            return 'News'
        case _:
            return ''
