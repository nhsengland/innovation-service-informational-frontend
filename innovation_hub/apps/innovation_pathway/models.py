from django.db import models
from django.db.models.aggregates import Count

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.contrib.typed_table_block.blocks import TypedTableBlock
from wagtail.core import blocks
from wagtail.fields import StreamField
from wagtail.search import index

from taggit.models import TaggedItemBase

from innovation_hub.apps.base.models import BasePage
from innovation_hub.apps.news.models import NewsDetailPage
from innovation_hub.apps.innovation_pathway.snippets import InnovationPathwayStageSnippet
from innovation_hub.config.blocks.stream_field_blocks import BLOCKS_BASE_LIST, ButtonLinkBlock, VerticalStepperBlock
from innovation_hub.config.helpers.templates_helper import add_heading_elements_id, heading_elements_ids_list


class InnovationPathwayStagePageTag(TaggedItemBase):
    content_object = ParentalKey('innovation_pathway.InnovationPathwayStagePage', related_name='tagged_items', on_delete=models.CASCADE)


class InnovationPathwayDetailPageTag(TaggedItemBase):
    content_object = ParentalKey('innovation_pathway.InnovationPathwayDetailPage', related_name='tagged_items', on_delete=models.CASCADE)


class InnovationPathwayIndexPage(BasePage):

    # Page rules.
    template = 'index_page.html'
    max_count = 1
    parent_page_types = ['home.HomePage']
    subpage_types = ['innovation_pathway.InnovationPathwayStagePage']

    # Database fields.
    content = StreamField(BLOCKS_BASE_LIST, collapsed=True, null=True, use_json_field=True)

    # Editor panels configuration.
    content_panels = BasePage.content_panels + [
        FieldPanel('content')
    ]

    def get_menu(self):
        children = self.get_children().live().public().specific()
        return list(map(lambda item: {'label': item.title, 'url': item.url}, children))

    class Meta:
        verbose_name = 'Innovation pathway index page'
        verbose_name_plural = 'Innovation pathway index page'


class InnovationPathwayStagePage(BasePage):

    # Page rules.
    template = 'index_page.html'
    max_count = 1
    parent_page_types = ['innovation_pathway.InnovationPathwayIndexPage']
    subpage_types = ['innovation_pathway.InnovationPathwayDetailPage']

    # Database fields.
    stage = models.ForeignKey(InnovationPathwayStageSnippet, null=True, blank=False, on_delete=models.SET_NULL, related_name='+')

    content = StreamField(BLOCKS_BASE_LIST, collapsed=True, null=True, use_json_field=True)

    tags = ClusterTaggableManager(through=InnovationPathwayStagePageTag, blank=True)

    # Editor panels configuration.
    content_panels = BasePage.content_panels + [
        FieldPanel('stage'),
        FieldPanel('content')
    ]
    promote_panels = BasePage.promote_panels + [
        FieldPanel('tags')
    ]

    # Search index configuration.
    search_fields = BasePage.search_fields + [
        index.RelatedFields('stage', [index.SearchField('name')]),
        index.RelatedFields('tags', [index.SearchField('name')])
    ]

    def get_menu(self):
        children = self.get_children().live().public().specific()
        return list(map(lambda item: {'label': item.title, 'url': item.url}, children))

    class Meta:
        verbose_name = 'Innovation pathway stage page'
        verbose_name_plural = 'Innovation pathway stages page'


class InnovationPathwayDetailPage(BasePage):

    # Page rules.
    template = 'detail_page.html'
    parent_page_types = ['innovation_pathway.InnovationPathwayStagePage']
    subpage_types = []

    # Database fields.
    stage = models.ForeignKey(InnovationPathwayStageSnippet, null=True, blank=False, on_delete=models.SET_NULL, related_name='+')

    content = StreamField(BLOCKS_BASE_LIST + [
        ('button_link', ButtonLinkBlock()),
        # ('content_separator', ContentSeparatorBlock()),
        # ('simple_text_card_group', SimpleTextCardGroupBlock()),
        ('table', TypedTableBlock([
            ('rich_text', blocks.RichTextBlock())
        ])),
        ('vertical_stepper', VerticalStepperBlock())
    ], collapsed=True, null=True, use_json_field=True)

    tags = ClusterTaggableManager(through=InnovationPathwayDetailPageTag, blank=True)

    # Editor panels configuration.
    content_panels = BasePage.content_panels + [
        FieldPanel('stage'),
        FieldPanel('content')
    ]
    promote_panels = BasePage.promote_panels + [
        FieldPanel('tags')
    ]

    # Search index configuration.
    search_fields = BasePage.search_fields + [
        index.RelatedFields('stage', [index.SearchField('name')]),
        index.RelatedFields('tags', [index.SearchField('name')])
    ]

    def get_context(self, request, *args, **kwargs):

        context = super().get_context(request, *args, **kwargs)

        page_tags = self.tags.all()

        related_content_news = NewsDetailPage.objects.live().public().filter(tags__in=page_tags)
        related_content_news = related_content_news.annotate(Count('title')).exclude(pk=self.pk).order_by('-title__count')[:3]
        related_content_ip = InnovationPathwayDetailPage.objects.live().public().filter(tags__in=page_tags)
        related_content_ip = related_content_ip.annotate(Count('title')).exclude(pk=self.pk).order_by('-title__count')[:3]

        context['related_content_list'] = [related_content_news, related_content_ip]
        return context

    def get_menu(self):

        children = self.get_siblings().public().live().specific()
        return list(map(lambda item: {
            'label': item.title,
            'url': item.url,
            'children': heading_elements_ids_list(str(item.content), r'2') if self.get_url().endswith(f'{item.slug}/') else None
        }, children))

    def get_parsed_html(self):
        return add_heading_elements_id(str(self.content))

    def previous_sibling(self):
        return self.get_prev_sibling()

    def next_sibling(self):
        return self.get_next_sibling()

    class Meta:
        verbose_name = 'Innovation pathway detail page'
        verbose_name_plural = 'Innovation pathway detail pages'
