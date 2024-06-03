from django.db import models

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey

from taggit.models import TaggedItemBase

from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.search import index

from is_homepage.apps.base.models import BasePage
from is_homepage.config.blocks import grid_layout_block


class GenericNavigationIndexPageTag(TaggedItemBase):
    content_object = ParentalKey('generic_navigation.GenericNavigationIndexPage', related_name='tagged_items', on_delete=models.CASCADE)


class GenericNavigationDetailPageTag(TaggedItemBase):
    content_object = ParentalKey('generic_navigation.GenericNavigationDetailPage', related_name='tagged_items', on_delete=models.CASCADE)


class GenericNavigationIndexPage(BasePage):

    # Page rules.
    template = 'generic_navigation_page.html'
    parent_page_types = ['home.HomePage']
    subpage_types = ['generic_navigation.GenericNavigationDetailPage']
    page_description = 'Choose this option to create content with a left side menu containing a list of child pages.'

    # Database fields.
    content = StreamField([grid_layout_block('two-thirds')], collapsed=True, blank=True, null=True, use_json_field=True)
    tags = ClusterTaggableManager(through=GenericNavigationIndexPageTag, blank=True)

    # Editor panels configuration.
    content_panels = BasePage.content_panels + [
        FieldPanel('content')
    ]
    promote_panels = BasePage.promote_panels + [
        FieldPanel('tags')
    ]

    # Search index configuration.
    search_fields = BasePage.search_fields + [
        index.RelatedFields('tags', [index.SearchField('name')])
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['navigation_pages'] = self.get_children().specific()
        context['search_params'] = request.GET.get('search', '')
        return context

    class Meta:
        verbose_name = 'Generic navigation bar page'
        verbose_name = 'Generic navigation bar pages'


class GenericNavigationDetailPage(BasePage):

    # Page rules.
    template = 'generic_navigation_page.html'
    parent_page_types = ['generic_navigation.GenericNavigationIndexPage']
    subpage_types = []

    # Database fields.
    content = StreamField([grid_layout_block('two-thirds')], collapsed=True, blank=True, null=True, use_json_field=True)
    tags = ClusterTaggableManager(through=GenericNavigationDetailPageTag, blank=True)

    # Editor panels configuration.
    content_panels = BasePage.content_panels + [
        FieldPanel('content')
    ]
    promote_panels = BasePage.promote_panels + [
        FieldPanel('tags')
    ]

    # Search index configuration.
    search_fields = BasePage.search_fields + [
        index.RelatedFields('tags', [index.SearchField('name')])
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['navigation_pages'] = self.get_siblings().specific()
        context['search_params'] = request.GET.get('search', '')
        return context

    def is_child_page(self):
        return True

    class Meta:
        verbose_name = 'Generic navigation bar detail page'
        verbose_name_plural = 'Generic navigation bar detail pages'
