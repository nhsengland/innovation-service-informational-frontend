from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page

from wagtailnhsukfrontend.blocks import ActionLinkBlock, CardGroupBlock, InsetTextBlock, RichTextBlock

from innovation_hub.config.blocks.stream_field_blocks import VerticalStepperBlock


class HomePage(Page):

    template = 'home/home_page.html'
    max_count = 1

    content = StreamField([
        ('rich_text', RichTextBlock()),
        ('action_link', ActionLinkBlock()),
        ('inset_text', InsetTextBlock()),
        ('card_group', CardGroupBlock()),
        ('vertical_stepper', VerticalStepperBlock())
    ], null=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('content')
    ]

    class Meta:
        verbose_name = 'Home page'
        verbose_name_plural = 'Home pages'
