from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class BannerBlock(blocks.StructBlock):

    banner_image = ImageChooserBlock(required=True)
    title = blocks.CharBlock(label='Title', required=True)
    supporting_text = blocks.CharBlock(label='Supporting text', required=False)
    call_to_action_label = blocks.CharBlock(required=False)
    call_to_action_page = blocks.PageChooserBlock(required=False)
    banner_height = blocks.IntegerBlock(required=False, help_text='Choose a numeric value in pixels. If empty, height will default to the chosen image height')
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


class ContentSeparatorBlock(blocks.StructBlock):
    """Empty block to make decisions on templates."""

    class Meta:
        icon = 'code'
        label = 'Content separator'
        label_format = 'Content separator'


class HeroBlock(blocks.StructBlock):

    heading = blocks.CharBlock(required=True)
    text = blocks.TextBlock(required=False)
    image = ImageChooserBlock(required=False)
    call_to_action_label = blocks.CharBlock(required=False)
    call_to_action_page = blocks.PageChooserBlock(required=False)

    class Meta:
        icon = 'user'
        label = 'Hero'
        label_format = 'Hero'
        template = 'blocks/hero_block.html'


class ImageGalleryBlock(blocks.StructBlock):

    columns = blocks.ChoiceBlock([(2, 2), (3, 3), (4, 4)], default=4, required=True, help_text='Choose the number of columns to show on each row (when viewing in desktop size.')
    row_height = blocks.IntegerBlock(required=False, help_text='Choose a numeric value in pixels.')

    gallery = blocks.ListBlock(
        blocks.StructBlock([
            ('column_span', blocks.ChoiceBlock([(1, 1), (2, 2), (3, 3), (4, 4)], default=1, required=True)),
            ('image', ImageChooserBlock(required=True)),
            ('url', blocks.URLBlock(required=False))
        ])
    )

    class Meta:
        icon = 'list-ol'
        label = 'Image gallery'
        label_format = 'Image gallery'
        template = 'blocks/image_gallery_block.html'


# class LayoutContainerBlock(blocks.StructBlock):

#     column = blocks.ChoiceBlock([
#         ('full', 'Full-width'),
#         ('one-half', 'One-half'),
#         ('one-third', 'One-third'),
#         ('two-thirds', 'Two-thirds'),
#     ], default='full', required=True)

#     class BodyStreamBlock(blocks.StreamBlock):
#         rich_text = blocks.RichTextBlock()
#         action_link = ActionLinkBlock()
#         inset_text = InsetTextBlock()

#     content = BodyStreamBlock(required=True)

#     class Meta:
#         icon = 'placeholder'
#         label = 'Layout container'
#         label_format = 'Layout container'
#         template = 'blocks/layout_container_block.html'


class IconTextCardGroupBlock(blocks.StructBlock):

    column = blocks.ChoiceBlock([
        ('full', 'Full width'),
        ('one-half', 'One half'),
        ('one-third', 'One third')
        # ('two-thirds', 'Two-thirds'),
    ], default='full', required=True)

    cards = blocks.ListBlock(
        blocks.StructBlock([
            ('icon', blocks.ChoiceBlock([
                ('success', 'Success icon'),
                ('error', 'Error icon')
            ], default='', required=False)),
            ('text', blocks.TextBlock(required=True))
        ], icon='arrow-right')
    )

    class Meta:
        icon = 'pilcrow'
        label = 'Icon text card'
        label_format = 'Icon text card'
        template = 'blocks/icon_text_card_group_block.html'


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
        template = 'blocks/vertical_stepper_block.html'
