from django.forms.utils import ErrorList

from wagtail.blocks import CharBlock, ChoiceBlock, IntegerBlock, ListBlock, PageChooserBlock, RichTextBlock, StreamBlock, StructBlock, StructValue, TextBlock, URLBlock
from wagtail.blocks.struct_block import StructBlockValidationError
from wagtail.contrib.typed_table_block.blocks import TypedTableBlock
from wagtail.images.blocks import ImageChooserBlock

from wagtailnhsukfrontend.blocks import ActionLinkBlock, InsetTextBlock, SummaryListBlock


class CommonBlockValues(StructValue):
    """
    Common block values class wiht generic methods to be used on templates.
    Note: Make sure that field names are equal on all classes using this one.
    """

    def get_full_url(self):
        """ Returns the linked page url, linked document url, or the exact URL. """
        link_page = self.get('link_page').url if self.get('link_page') else None
        link_url = self.get('link_url')
        link_document = self.get('link_document').url if self.get('link_document') else None
        return link_page or link_url or link_document

    def get_open_new_window(self):
        return True if self.get('link_url') else False


class BannerBlock(StructBlock):

    background_image = ImageChooserBlock(required=True)
    title = CharBlock(label='Title', required=True)
    supporting_text = CharBlock(label='Supporting text', required=False)
    link_label = CharBlock(label='Call to action label', required=False)
    link_page = PageChooserBlock(label='Call to action page', required=False)
    link_url = URLBlock(label='Call to action url', required=False)
    banner_height = IntegerBlock(required=False, help_text='Choose a numeric value in pixels. If empty, height will default to the chosen image height')
    layout = ChoiceBlock([('title-text', 'Title - Text'), ('text-title', 'Text - Title')], default='title-text', required=True)
    alignment = ChoiceBlock([('left', 'Left'), ('center', 'Center')], default='left', required=True)

    def clean(self, value):
        errors = {}
        if value.get('link_page') and value.get('link_url'):
            errors['link_page'] = errors['link_url'] = ErrorList(['Please select a call to action page or url (but not both)'])
        if errors:
            raise StructBlockValidationError(block_errors=errors)
        return super().clean(value)

    class Meta:
        icon = 'rectangle-ad'
        label = 'Banner'
        label_format = 'Banner: {title}'
        template = 'blocks/banner_block.html'
        value_class = CommonBlockValues


class ButtonBlock(StructBlock):

    link_label = CharBlock(label='Label', required=True)
    link_page = PageChooserBlock(label='Internal page', required=False)
    link_url = URLBlock(label='External url', required=False)

    def clean(self, value):
        errors = {}
        if not (bool(value.get('link_page')) ^ bool(value.get('link_url'))):
            errors['link_page'] = errors['link_url'] = ErrorList(['Please select an internal page or an external url (but not both)'])
        if errors:
            raise StructBlockValidationError(block_errors=errors)
        return super().clean(value)

    class Meta:
        icon = 'square-arrow-up-right'
        label = 'Button'
        label_format = 'Button: {link_label}'
        template = 'blocks/button_block.html'
        value_class = CommonBlockValues


class CollapsibleDetailsBlock(StructBlock):

    class BodyStreamBlock(StreamBlock):
        description_list = SummaryListBlock(group='Lists', label='Description list', label_format='Description list: {rows}')
        table = TypedTableBlock([('rich_text', RichTextBlock())], group='Lists')
        action_link = ActionLinkBlock(group='Navigation', label='Action link', label_format='Action link: {text}')
        inset_text = InsetTextBlock(group='Text', label='Inset text', label_format='Inset text: {body}', icon='indent')
        rich_text = RichTextBlock(group='Text')

    title = CharBlock(required=True)
    content = BodyStreamBlock(required=True)

    class Meta:
        icon = 'collapse-down'
        template = 'blocks/collapsible_details_block.html'


class HeadingBlock(StructBlock):

    column_width = ChoiceBlock([('full', 'Full'), ('one-half', 'One half'), ('two-thirds', 'Two thirds')], default='full', required=True)
    heading = CharBlock(group='Page', label='Page heading', help_text='This is a H1 heading, and only one per page is allowed. For different heading levels, please use Rich text.')
    # heading_level = ChoiceBlock((1, 1), [(2, 2), (3, 3), (4, 4)], default=1, required=True)

    class Meta:
        icon = 'title'
        label = 'Heading'
        label_format = 'Heading: {heading}'
        template = 'blocks/heading_block.html'


class HeroBlock(StructBlock):

    heading = CharBlock(required=True)
    text = TextBlock(required=False)
    link_label = CharBlock(label='Call to action label', required=False)
    link_page = PageChooserBlock(label='Call to action page', required=False)
    link_url = URLBlock(label='Call to action url', required=False)
    image = ImageChooserBlock(required=False)

    def clean(self, value):
        errors = {}
        if value.get('link_page') and value.get('link_url'):
            errors['link_page'] = errors['link_url'] = ErrorList(['Please select a call to action page or url (but not both)'])
        if errors:
            raise StructBlockValidationError(block_errors=errors)
        return super().clean(value)

    class Meta:
        icon = 'crown'
        label = 'Hero'
        label_format = 'Hero: {heading}'
        template = 'blocks/hero_block.html'
        value_class = CommonBlockValues


class TextCardGroupBlock(StructBlock):

    column_width = ChoiceBlock([('full', 'Full'), ('one-half', 'One half'), ('one-third', 'One third')], default='full', required=True)
    cards = ListBlock(
        StructBlock([
            ('icon', ChoiceBlock([('success', 'Success icon'), ('error', 'Error icon'), ('bullet', 'Bullet icon')], default='success', required=False)),
            ('text', TextBlock(required=True))
        ], label='Card', label_format='Card: {text}', icon='square-check-regular')
    )

    class Meta:
        icon = 'square-check-solid'
        label = 'Text cards'
        label_format = 'Text cards: {cards}'
        template = 'blocks/text_card_group_block.html'


class ImageGalleryBlock(StructBlock):

    columns = ChoiceBlock([(2, 2), (3, 3), (4, 4)], default=4, required=True, help_text='Choose the number of columns to show on each row (when viewing in desktop size.')
    row_height = IntegerBlock(required=False, help_text='Choose a numeric value in pixels.')

    gallery = ListBlock(
        StructBlock([
            ('column_span', ChoiceBlock([(1, 1), (2, 2), (3, 3), (4, 4)], default=1, required=True)),
            ('image', ImageChooserBlock(required=True)),
            ('url', URLBlock(required=False))
        ])
    )

    class Meta:
        icon = 'images'
        label = 'Image gallery'
        label_format = 'Image gallery: {gallery}'
        template = 'blocks/image_gallery_block.html'


class VerticalStepperBlock(StructBlock):

    steps = ListBlock(
        StructBlock([
            ('title', CharBlock(required=True, max_length=100)),
            ('text', TextBlock(required=True))
        ], label='Step', label_format='Step: {title}', icon='list-check')
    )

    class Meta:
        icon = 'list-ol'
        label = 'Vertical stepper'
        label_format = 'Vertical stepper: {steps}'
        template = 'blocks/vertical_stepper_block.html'
