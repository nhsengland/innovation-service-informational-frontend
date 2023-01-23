from wagtail.admin.edit_handlers import FieldPanel
from wagtail.fields import StreamField

from innovation_hub.apps.base.models import BasePage
from innovation_hub.config.blocks.stream_field_blocks import BLOCKS_BASE_LIST, BannerBlock, ButtonLinkBlock, ContentSeparatorBlock, SimpleTextCardGroupBlock, VerticalStepperBlock


class GenericPage(BasePage):

    # Page rules.
    template = 'generic_page.html'
    parent_page_types = ['home.HomePage']

    # Database fields.
    content = StreamField(BLOCKS_BASE_LIST + [
        ('banner', BannerBlock()),
        ('button_link', ButtonLinkBlock()),
        ('content_separator', ContentSeparatorBlock()),
        ('simple_text_card_group', SimpleTextCardGroupBlock()),
        ('vertical_stepper', VerticalStepperBlock())
    ], collapsed=True, blank=True, null=True, use_json_field=True)

    # Editor panels configuration.
    content_panels = BasePage.content_panels + [
        FieldPanel('content')
    ]

    class Meta:
        verbose_name = 'Generic page'
        verbose_name_plural = 'Generic page'
