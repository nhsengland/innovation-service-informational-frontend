from django.db import models
from django.db.models.aggregates import Count

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager

from wagtail.admin.panels import FieldPanel
from wagtail.documents.models import Document
from wagtail.fields import StreamField
from wagtail.search import index

from wagtail_pdf_view.mixins import PdfViewPageMixin
from taggit.models import TaggedItemBase

from is_homepage.apps.base.models import BasePage
from is_homepage.apps.innovation_guides.snippets import InnovationGuidesStageSnippet
from is_homepage.config.blocks import FIXED_LAYOUT_BLOCK, FLUID_LAYOUT_BLOCK, grid_layout_block


class InnovationGuidesStagePageTag(TaggedItemBase):
    content_object = ParentalKey('innovation_guides.InnovationGuidesStagePage', related_name='tagged_items', on_delete=models.CASCADE)


class InnovationGuidesDetailPageTag(TaggedItemBase):
    content_object = ParentalKey('innovation_guides.InnovationGuidesDetailPage', related_name='tagged_items', on_delete=models.CASCADE)


class InnovationGuidesIndexPage(PdfViewPageMixin, BasePage):

    # Page rules.
    template = 'index_page.html'
    max_count = 1
    parent_page_types = ['home.HomePage']
    subpage_types = ['innovation_guides.InnovationGuidesStagePage']
    ROUTE_CONFIG = [('html', r'^$'), ('pdf', r'^pdf/$')]  # Printing configuration.

    # Database fields.
    intro = StreamField([FIXED_LAYOUT_BLOCK, FLUID_LAYOUT_BLOCK], collapsed=True, blank=True, null=True, use_json_field=True, help_text='This content appears before stages list')
    content = StreamField([FIXED_LAYOUT_BLOCK, FLUID_LAYOUT_BLOCK], collapsed=True, blank=True, null=True, use_json_field=True, help_text='This content appears after stages list')

    # Editor panels configuration.
    content_panels = BasePage.content_panels + [
        FieldPanel('intro'),
        FieldPanel('content')
    ]

    def get_context(self, request, mode=None, **kwargs):

        context = super().get_context(request, **kwargs)

        if mode == 'pdf':
            self.template = 'index_page_print.html'

        return context

    class Meta:
        verbose_name = 'Innovation guides index page'
        verbose_name_plural = 'Innovation guides index page'


class InnovationGuidesStagePage(PdfViewPageMixin, BasePage):

    # Page rules.
    template = 'stage_page.html'
    parent_page_types = ['innovation_guides.InnovationGuidesIndexPage']
    subpage_types = ['innovation_guides.InnovationGuidesDetailPage']
    ROUTE_CONFIG = [('html', r'^$'), ('pdf', r'^pdf/$')]  # Printing configuration.

    # Database fields.
    stage = models.ForeignKey(InnovationGuidesStageSnippet, null=True, blank=False, on_delete=models.SET_NULL, related_name='+')
    content = StreamField([grid_layout_block('two-thirds')], collapsed=True, blank=True, null=True, use_json_field=True)
    tags = ClusterTaggableManager(through=InnovationGuidesStagePageTag, blank=True)

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

    def get_context(self, request, mode=None, **kwargs):

        context = super().get_context(request, **kwargs)

        if mode == 'pdf':
            self.template = 'stage_page_print.html'

        return context

    class Meta:
        verbose_name = 'Innovation guides stage page'
        verbose_name_plural = 'Innovation guides stages page'


class InnovationGuidesDetailPage(PdfViewPageMixin, BasePage):

    # Page rules.
    template = 'detail_page.html'
    parent_page_types = ['innovation_guides.InnovationGuidesStagePage']
    subpage_types = []
    ROUTE_CONFIG = [('html', r'^$'), ('pdf', r'^pdf/$')]  # Printing configuration.

    # Database fields.
    stage = models.ForeignKey(InnovationGuidesStageSnippet, null=True, blank=False, on_delete=models.SET_NULL, related_name='+')
    content = StreamField([grid_layout_block('two-thirds')], collapsed=True, blank=True, null=True, use_json_field=True)
    tags = ClusterTaggableManager(through=InnovationGuidesDetailPageTag, blank=True)

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

    def get_context(self, request, mode=None, **kwargs):

        from is_homepage.apps.case_studies.models import CaseStudiesDetailPage
        from is_homepage.apps.help_resources.models import HelpResourcesMenuItemPage
        from is_homepage.apps.news.models import NewsDetailPage

        context = super().get_context(request, **kwargs)

        if mode == 'pdf':
            self.template = 'detail_page_print.html'

        else:

            page_tags = self.tags.all()

            related_content_news = NewsDetailPage.objects.live().public().filter(tags__in=page_tags)
            related_content_news = related_content_news.annotate(Count('title')).exclude(pk=self.pk).order_by('-title__count')[:3]
            related_content_ig = InnovationGuidesDetailPage.objects.live().public().filter(tags__in=page_tags)
            related_content_ig = related_content_ig.annotate(Count('title')).exclude(pk=self.pk).order_by('-title__count')[:3]
            related_content_case_studies = CaseStudiesDetailPage.objects.live().public().filter(tags__in=page_tags)
            related_content_case_studies = related_content_case_studies.annotate(Count('title')).exclude(pk=self.pk).order_by('-title__count')[:3]
            related_help_resources = HelpResourcesMenuItemPage.objects.live().public().filter(tags__in=page_tags)
            related_help_resources = related_help_resources.annotate(Count('title')).exclude(pk=self.pk).order_by('-title__count')[:3]
            related_documents = Document.objects.filter(tags__in=page_tags)
            related_documents = related_documents.annotate(Count('title')).exclude(pk=self.pk).order_by('-title__count')[:3]

            context['related_content_list'] = [related_content_news, related_content_ig, related_content_case_studies, related_help_resources, related_documents]
            context['related_content_count'] = sum([len(items) for items in context['related_content_list']])

        return context

    class Meta:
        verbose_name = 'Innovation guides detail page'
        verbose_name_plural = 'Innovation guides detail pages'
