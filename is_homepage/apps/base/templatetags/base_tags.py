import re

from django import template
from django.utils.safestring import mark_safe
from django.utils.text import slugify

register = template.Library()


@register.simple_tag(takes_context=True)
def seo_canonical(context):
    """
    Returns the canonical tag.
    Example: For the url https://some-url.com?queryParam=seo google would index this as a separate page, just because we have a queryParam, splitting your page hits and affecting your ranking.
    You'll also start to get errors on Search Console where Google has selected what its algorithms decide is the canonical page for you.
    In this case, we want to tell Google that the url without the query string is the canonical url.
    """

    page_canonical_url = context.request.build_absolute_uri(context.request.path)
    if page_canonical_url:
        return mark_safe(f'<link rel="canonical" href="{page_canonical_url}">')
    else:
        return ''


@register.simple_tag
def html_headings_parse(html, element_h_number, *args):
    """
    Parse HTML headings (<h1-6>) and performs some operations

    Input:
    element_h_number:   This parameter accepts a regexp, for example: '1', '1,2' or '1-6'

    Allowed operations:
    add-id-attribute:   Adds an "id" attribute with a slugfied content based on the title/content, usually to be able to use relative links (#some-link).
    replace-level:      Replace heading level. This is mostly used in some printing scenarios where <h2> needs to be <h1>.
    """

    allowed_actions = ['add-id-attribute', 'replace-level']

    actions = {}
    for item in args:
        action = [arg.strip() for arg in item.split(':')]
        if action[0] in allowed_actions:
            actions[action[0]] = action[1] if len(action) == 2 else None

    def __replace_actions(match):

        element_h_number = actions['replace-level'] if 'replace-level' in actions else match.group(1)
        element_attributes = match.group(2)
        element_content = match.group(3)
        element_id = f' id="{slugify(element_content)}"' if 'add-id-attribute' in actions else ''

        # print(f'<h{element_h_number}{element_id}{element_attributes}>{ element_content }</h{element_h_number}>')

        return f'<h{element_h_number}{element_id}{element_attributes}>{ element_content }</h{element_h_number}>'

    return mark_safe(re.sub(rf'<h([{element_h_number}])([^>]*)>((\n|.)+?)</h\1>', __replace_actions, str(html)))


@register.simple_tag
def html_headings_elements_list(html, heading_levels_regexp=r'1-6'):
    """
    Returns a list with all the header tags found in the html.
    This list includes a title and a slugfied link to be able to use relative links (#some-link)
    """
    matches = re.findall(rf'<h([{heading_levels_regexp}])([^>]*)>((\n|.)+?)</h\1>', str(html))
    return list(map(lambda x: {'title': x[2], 'slug': slugify(x[2])}, matches))


@register.tag(name='blocktovariable')
def do_blocktovariable(parser, token):
    """
    This tag can transform the content of a block into a variable inside a template.
    With this, is possible to verify if it exists and act accordingly.
    """

    try:
        tag_name, args = token.contents.split(None, 1)

    except ValueError:
        raise template.TemplateSyntaxError("'blocktovariable' node requires a variable name.")

    nodelist = parser.parse(('endblocktovariable',))
    parser.delete_first_token()

    return BlockToVariableNode(nodelist, args)


class BlockToVariableNode(template.Node):

    def __init__(self, nodelist, varname):
        self.nodelist = nodelist
        self.varname = varname

    def render(self, context):
        output = self.nodelist.render(context)
        context[self.varname] = output
        return ''
