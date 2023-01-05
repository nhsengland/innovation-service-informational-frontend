from wagtail.core import blocks

from wagtailnhsukfrontend.blocks import ActionLinkBlock, CardGroupBlock, InsetTextBlock


class ButtonLinkBlock(blocks.StructBlock):

    text = blocks.CharBlock(label='Link text', required=True)
    internal_page = blocks.PageChooserBlock(label='Internal Page', required=True)

    class Meta:
        icon = 'doc-full'
        template = 'blocks/button_link_block.html'


class VerticalStepperBlock(blocks.StructBlock):

    steps = blocks.ListBlock(
        blocks.StructBlock([
            ('title', blocks.CharBlock(required=True, max_length=100)),
            ('text', blocks.TextBlock(required=True))
        ])
    )

    class Meta:
        template = "blocks/vertical_stepper_block.html"
        icon = "list-ol"
        label = "Vertical stepper"


class ContentSeparatorBlock(blocks.StructBlock):
    """Empty block to make decisions on templates. """

    class Meta:
        icon = 'code'
        label = "Content separator"


class LayoutContainerBlock(blocks.StructBlock):

    column = blocks.ChoiceBlock([
        ('full', 'Full-width'),
        ('one-half', 'One-half'),
        ('one-third', 'One-third'),
        ('two-thirds', 'Two-thirds'),
    ], default='full', required=True)

    class BodyStreamBlock(blocks.StreamBlock):
        rich_text = blocks.RichTextBlock()
        action_link = ActionLinkBlock()
        inset_text = InsetTextBlock()

    content = BodyStreamBlock(required=True)

    class Meta:
        icon = 'placeholder'
        template = 'blocks/layout_container_block.html'


class SimpleTextCardGroupBlock(blocks.StructBlock):

    column = blocks.ChoiceBlock([
        ('full', 'Full-width'),
        ('one-half', 'One-half'),
        ('one-third', 'One-third'),
        # ('two-thirds', 'Two-thirds'),
    ], default='full', required=True)

    cards = blocks.ListBlock(
        blocks.StructBlock([
            ('icon', blocks.ChoiceBlock([
                ('green-check', 'Green check'),
                ('red-x-mark', 'Red X mark')
            ], default='', required=False)),
            ('text', blocks.TextBlock(required=True))
        ], icon='arrow-right')
    )

    class Meta:
        icon = 'pilcrow'
        template = 'blocks/simple_text_card_group_block.html'


BLOCKS_BASE_LIST = [
    ('rich_text', blocks.RichTextBlock()),
    ('action_link', ActionLinkBlock()),
    ('inset_text', InsetTextBlock()),
    ('card_group', CardGroupBlock()),
    ('vertical_stepper', VerticalStepperBlock()),
    ('layout_container', LayoutContainerBlock())
]
