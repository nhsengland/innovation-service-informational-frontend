from django import template

register = template.Library()


@register.tag(name='blocktovariable')
def do_blocktovariable(parser, token):
    """
    This tag can transform the content of a block into a variable inside a template.
    With this, is possible to verify if it exists and act accordingly. (used on base.html file)
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
