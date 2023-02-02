from django import template

register = template.Library()


@register.filter
def classname(obj):
    return obj.__class__.__name__


@register.filter
def pagetypename(obj):
    match obj.__class__.__name__:
        case 'NewsDetailPage':
            return 'News'
        case 'InnovationPathwayDetailPage':
            return 'Innovation pathway'
        case 'CaseStudiesDetailPage':
            return 'Case Studies'
        case _:
            return ''
