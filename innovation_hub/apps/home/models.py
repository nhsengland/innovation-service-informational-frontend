from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core import blocks
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock

from innovation_hub.apps.base.models import BasePage
from innovation_hub.apps.news.models import NewsDetailPage
from innovation_hub.config.blocks.stream_field_blocks import BLOCKS_BASE_LIST, BannerBlock, ButtonLinkBlock, ContentSeparatorBlock, SimpleTextCardGroupBlock, VerticalStepperBlock


class HomePage(BasePage):

    # Page rules.
    template = 'home_page.html'
    max_count = 1

    # Database fields.
    content = StreamField(BLOCKS_BASE_LIST + [
        ('hero', blocks.StructBlock([
            ('heading', blocks.CharBlock(required=False)),
            ('text', blocks.TextBlock(required=False)),
            ('image', ImageChooserBlock(required=False)),
            ('call_to_action_label', blocks.CharBlock(required=False)),
            ('call_to_action_page', blocks.PageChooserBlock(required=False))
        ], icon='user')),
        ('banner', BannerBlock()),
        ('button_link', ButtonLinkBlock()),
        ('content_separator', ContentSeparatorBlock()),
        ('simple_text_card_group', SimpleTextCardGroupBlock()),
        ('vertical_stepper', VerticalStepperBlock())
    ], block_counts={'hero': {'max_num': 1}, 'banner': {'max_num': 1}}, collapsed=True, null=True, use_json_field=True)

    # Editor panels configuration.
    content_panels = BasePage.content_panels + [
        FieldPanel('content')
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['news_list'] = NewsDetailPage.objects.live().public().order_by('-first_published_at')[0:3]
        return context

    class Meta:
        verbose_name = 'Home page'
        verbose_name_plural = 'Home pages'
