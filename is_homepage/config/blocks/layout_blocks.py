from wagtail.blocks import ChoiceBlock, ListBlock, RichTextBlock, StreamBlock, StructBlock
from wagtail.contrib.typed_table_block.blocks import TypedTableBlock

from wagtailnhsukfrontend.blocks import ActionLinkBlock, InsetTextBlock, SummaryListBlock

from .custom_blocks import BannerBlock, ButtonBlock, CollapsibleDetailsBlock, ImageGalleryBlock, TextCardGroupBlock, VerticalStepperBlock
from .extended_blocks import CardGroupBlock


FIXED_LAYOUT_BLOCKS_LIST = [

    ('card_group', CardGroupBlock(group='Components', label='Cards', label_format='Cards', icon='rectangle-list-regular')),
    ('collapsible_details', CollapsibleDetailsBlock(group='Components')),
    ('text_card_group', TextCardGroupBlock(group='Components')),

    ('banner', BannerBlock(group='Images')),
    ('image_gallery', ImageGalleryBlock(group='Images')),

    ('description_list', SummaryListBlock(group='Lists', label='Description list', label_format='Description list: {rows}')),
    ('table', TypedTableBlock([('rich_text', RichTextBlock())], group='Lists')),
    ('vertical_stepper', VerticalStepperBlock(group='Lists')),

    ('action_link', ActionLinkBlock(group='Navigation', label='Action link', label_format='Action link: {text}')),
    ('button_link', ButtonBlock(group='Navigation')),

    ('inset_text', InsetTextBlock(group='Text', label='Inset text', label_format='Inset text: {body}', icon='indent')),
    ('rich_text', RichTextBlock(group='Text'))

]

FLUID_LAYOUT_BLOCKS_LIST = [
    ('banner', BannerBlock(group='Images'))
]


def grid_layout_block(container_width):

    match container_width:
        case 'two-thirds':
            choices = [('full', 'Full'), ('one-half', 'One half')]
        case _:
            choices = [('full', 'Full'), ('one-half', 'One half'), ('one-third', 'One third'), ('two-thirds', 'Two thirds'), ('one-quarter', 'One quarter'), ('three-quarters', 'Three-quarters')]

    return ('layout_grid', ListBlock(
        StructBlock([
            ('column_width', ChoiceBlock(choices, label='Width', default='full', required=True)),
            ('content', StreamBlock(FIXED_LAYOUT_BLOCKS_LIST + FLUID_LAYOUT_BLOCKS_LIST, collapsed=True, blank=True, null=True, use_json_field=True))
        ], label='Column', label_format='Column: {column_width}', icon='square-check-regular'),
        group='Layout'
    ))


FIXED_LAYOUT_BLOCK = ('fixed', StructBlock([
    ('background_color', ChoiceBlock([('default', 'Default'), ('white', 'White')], default='default', required=True)),
    grid_layout_block('full')
], group='Layout', label='Fixed layout', label_format='Fixed layout: {background_color} background color', icon='layout-three-columns'))

FLUID_LAYOUT_BLOCK = ('fluid', StructBlock([
    ('background_color', ChoiceBlock([('default', 'Default'), ('white', 'White')], default='default', required=True)),
    ('content', StreamBlock(FLUID_LAYOUT_BLOCKS_LIST, collapsed=True, blank=True, null=True, use_json_field=True))
], group='Layout', label='Fluid layout', label_format='Fluid layout: {background_color} background color', icon='columns-gap'))
