from wagtail.core import blocks
from wagtail.contrib.typed_table_block.blocks import TypedTableBlock

from wagtailnhsukfrontend.blocks import ActionLinkBlock, CardGroupBlock, InsetTextBlock

from .custom_blocks import BannerBlock, ButtonLinkBlock, ImageGalleryBlock, IconTextCardGroupBlock, VerticalStepperBlock


FIXED_LAYOUT_BLOCKS_LIST = [

    ('inset_text', InsetTextBlock(group='Text')),
    ('rich_text', blocks.RichTextBlock(group='Text')),

    ('action_link', ActionLinkBlock(group='Buttons and Links')),
    ('button_link', ButtonLinkBlock(group='Buttons and Links')),

    # ('layout_container', LayoutContainerBlock(group='Components', label='Layout container')),
    ('table', TypedTableBlock([('rich_text', blocks.RichTextBlock())], group='Components')),

    ('card_group', CardGroupBlock(group='Components', label='NHS Cards')),
    ('icon_text_card_group', IconTextCardGroupBlock(group='Components', label='Icon text cards')),
    ('vertical_stepper', VerticalStepperBlock(group='Components', label='Vertical stepper')),

    ('banner', BannerBlock(group='Images')),
    ('image_gallery', ImageGalleryBlock(group='Images'))

]

FLUID_LAYOUT_BLOCKS_LIST = [
    ('banner', BannerBlock(group='Images'))
]


FIXED_LAYOUT_BLOCK = [('fixed', blocks.StructBlock([
    ('background_color', blocks.ChoiceBlock([('default', 'Default'), ('white', 'White')], default='default', required=True)),
    ('column', blocks.ChoiceBlock([('full', 'Full width'), ('one-half', 'One half'), ('one-third', 'One third'), ('two-thirds', 'Two thirds')], default='full', required=True)),
    ('content', blocks.StreamBlock(FIXED_LAYOUT_BLOCKS_LIST + FLUID_LAYOUT_BLOCKS_LIST, collapsed=True, blank=True, null=True, use_json_field=True))
], label='Fixed layout', icon='resubmit'))]

FLUID_LAYOUT_BLOCK = [('fluid', blocks.StructBlock([
    ('background_color', blocks.ChoiceBlock([('default', 'Default'), ('white', 'White')], default='default', required=True)),
    ('content', blocks.StreamBlock(FLUID_LAYOUT_BLOCKS_LIST, collapsed=True, blank=True, null=True, use_json_field=True))
], label='Fluid layout', icon='resubmit'))]
