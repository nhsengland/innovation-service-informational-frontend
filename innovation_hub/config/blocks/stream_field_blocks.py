from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

from wagtailnhsukfrontend.blocks import ActionLinkBlock, CardGroupBlock, InsetTextBlock


class BannerBlock(blocks.StructBlock):

    banner_image = ImageChooserBlock(required=True)
    title = blocks.CharBlock(label='Title', required=True)
    supporting_text = blocks.CharBlock(label='Supporting text', required=False)
    layout = blocks.ChoiceBlock([
        ('title-text', 'Title - Text'),
        ('text-title', 'Text - Title')
    ], default='title-text', required=True)
    alignment = blocks.ChoiceBlock([
        ('left', 'Left'),
        ('center', 'Center')
    ], default='left', required=True)

    class Meta:
        icon = 'snippet'
        label = 'Banner'
        label_format = 'Banner'
        template = 'blocks/banner_block.html'


class ButtonLinkBlock(blocks.StructBlock):

    text = blocks.CharBlock(label='Link text', required=True)
    internal_page = blocks.PageChooserBlock(label='Internal Page', required=True)

    class Meta:
        icon = 'doc-full'
        label = 'Button link'
        label_format = 'Button link'
        template = 'blocks/button_link_block.html'


class VerticalStepperBlock(blocks.StructBlock):

    steps = blocks.ListBlock(
        blocks.StructBlock([
            ('title', blocks.CharBlock(required=True, max_length=100)),
            ('text', blocks.TextBlock(required=True))
        ])
    )

    class Meta:
        icon = 'list-ol'
        label = 'Vertical stepper'
        label_format = 'Vertical stepper'
        template = "blocks/vertical_stepper_block.html"


class ContentSeparatorBlock(blocks.StructBlock):
    """Empty block to make decisions on templates. """

    class Meta:
        icon = 'code'
        label = 'Content separator'
        label_format = 'Content separator'


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
        label = 'Layout container'
        label_format = 'Layout container'
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
        label = 'Simple text card'
        label_format = 'Simple text card'
        template = 'blocks/simple_text_card_group_block.html'


BLOCKS_BASE_LIST = [
    ('action_link', ActionLinkBlock()),
    ('card_group', CardGroupBlock()),
    ('inset_text', InsetTextBlock()),
    ('layout_container', LayoutContainerBlock()),
    ('rich_text', blocks.RichTextBlock())
]
