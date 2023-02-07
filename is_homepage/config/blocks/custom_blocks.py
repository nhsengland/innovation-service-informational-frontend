from django.forms.utils import ErrorList

from wagtail.blocks import CharBlock, ChoiceBlock, IntegerBlock, ListBlock, PageChooserBlock, URLBlock, StructBlock, StructValue, TextBlock
from wagtail.blocks.struct_block import StructBlockValidationError
from wagtail.images.blocks import ImageChooserBlock


class CommonBlockValues(StructValue):
    """
    Common block values class wiht generic methods to be used on templates.
    Note: Make sure that field names are equal on all classes using this one.
    """

    def link_url(self):
        """ Returns the linked page url, linked document url, or the exact URL. """
        link_page = self.get('link_page')
        link_url = self.get('link_url')
        link_document = self.get('link_document')
        return link_page.url or link_url or link_document.url


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


class IconTextCardGroupBlock(StructBlock):

    column = ChoiceBlock([
        ('full', 'Full width'),
        ('one-half', 'One half'),
        ('one-third', 'One third')
    ], default='full', required=True)

    cards = ListBlock(
        StructBlock([
            ('icon', ChoiceBlock([
                ('success', 'Success icon'),
                ('error', 'Error icon')
            ], default='', required=False)),
            ('text', TextBlock(required=True))
        ], label='Card', label_format='Card: {text}', icon='square-check-regular')
    )

    class Meta:
        icon = 'square-check-solid'
        label = 'Icon text cards'
        label_format = 'Icon text cards: {cards}'
        template = 'blocks/icon_text_card_group_block.html'


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
