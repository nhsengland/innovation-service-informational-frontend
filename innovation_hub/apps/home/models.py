# from django.db import models

from wagtail.admin.edit_handlers import FieldPanel
# from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PageChooserPanel
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.blocks import ImageChooserBlock

from innovation_hub.apps.news.models import NewsDetailPage
from innovation_hub.config.blocks.stream_field_blocks import BLOCKS_BASE_LIST, ButtonLinkBlock, ContentSeparatorBlock, SimpleTextCardGroupBlock


class HomePage(Page):

    template = 'home/home_page.html'
    max_count = 1

    # hero_heading = models.TextField(blank=True, null=True, default='')
    # hero_text = models.TextField(blank=True, null=True)
    # hero_image = models.ForeignKey('wagtailimages.Image', blank=True, null=True, related_name='+', on_delete=models.SET_NULL)
    # hero_url = models.URLField(blank=True, null=True)

    content = StreamField(BLOCKS_BASE_LIST + [
        ('hero', blocks.StructBlock([
            ('heading', blocks.CharBlock(required=False)),
            ('text', blocks.TextBlock(required=False)),
            ('image', ImageChooserBlock(required=False)),
            ('call_to_action_label', blocks.CharBlock(required=False)),
            ('call_to_action_page', blocks.PageChooserBlock(required=False))
        ], icon='user')),
        ('simple_text_card_group', SimpleTextCardGroupBlock()),
        ('button_link', ButtonLinkBlock()),
        ('content_separator', ContentSeparatorBlock())
    ], block_counts={'hero': {'max_num': 1}}, collapsed=True, null=True, use_json_field=True)

    content_panels = Page.content_panels + [
        # MultiFieldPanel([
        #     FieldPanel('hero_heading'),
        #     FieldPanel('hero_text'),
        #     FieldPanel('hero_image'),
        #     PageChooserPanel('hero_url')
        # ], heading="Hero section"),
        FieldPanel('content')
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['news_list'] = NewsDetailPage.objects.live().public().order_by('-first_published_at')[1:4]
        return context

    class Meta:
        verbose_name = 'Home page'
        verbose_name_plural = 'Home pages'
