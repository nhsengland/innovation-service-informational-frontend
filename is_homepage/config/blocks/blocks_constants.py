from wagtail.blocks import ChoiceBlock, RichTextBlock, StreamBlock, StructBlock
from wagtail.contrib.typed_table_block.blocks import TypedTableBlock

from wagtailnhsukfrontend.blocks import ActionLinkBlock, CardGroupBlock, InsetTextBlock

from .custom_blocks import BannerBlock, ButtonBlock, ImageGalleryBlock, IconTextCardGroupBlock, VerticalStepperBlock


FIXED_LAYOUT_BLOCKS_LIST = [

    ('inset_text', InsetTextBlock(group='Text', label='Inset text', label_format='Inset text: {body}', icon='indent')),
    ('rich_text', RichTextBlock(group='Text')),

    ('action_link', ActionLinkBlock(group='Buttons and Links', label='Action link', label_format='Action link: {text}')),
    ('button_link', ButtonBlock(group='Buttons and Links')),

    ('table', TypedTableBlock([('rich_text', RichTextBlock())], group='Components')),

    ('card_group', CardGroupBlock(group='Components', label='Cards', label_format='Cards', icon='rectangle-list-regular')),
    ('icon_text_card_group', IconTextCardGroupBlock(group='Components')),
    ('vertical_stepper', VerticalStepperBlock(group='Components')),

    ('banner', BannerBlock(group='Images')),
    ('image_gallery', ImageGalleryBlock(group='Images'))

]

FLUID_LAYOUT_BLOCKS_LIST = [
    ('banner', BannerBlock(group='Images'))
]


FIXED_LAYOUT_BLOCK = [('fixed', StructBlock([
    ('background_color', ChoiceBlock([('default', 'Default'), ('white', 'White')], default='default', required=True)),
    ('column', ChoiceBlock([('full', 'Full width'), ('one-half', 'One half'), ('one-third', 'One third'), ('two-thirds', 'Two thirds')], default='full', required=True)),
    ('content', StreamBlock(FIXED_LAYOUT_BLOCKS_LIST + FLUID_LAYOUT_BLOCKS_LIST, collapsed=True, blank=True, null=True, use_json_field=True))
], label='Fixed layout', label_format='Fixed layout: {background_color} background', icon='layout-three-columns'))]

FLUID_LAYOUT_BLOCK = [('fluid', StructBlock([
    ('background_color', ChoiceBlock([('default', 'Default'), ('white', 'White')], default='default', required=True)),
    ('content', StreamBlock(FLUID_LAYOUT_BLOCKS_LIST, collapsed=True, blank=True, null=True, use_json_field=True))
], label='Fluid layout', label_format='Fluid layout: {background_color} background', icon='columns-gap'))]

