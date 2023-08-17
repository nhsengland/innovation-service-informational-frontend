from django.db import models

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey

from taggit.models import TaggedItemBase

from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.search import index

from is_homepage.apps.base.models import BasePage
from is_homepage.config.blocks import FIXED_LAYOUT_BLOCK, FLUID_LAYOUT_BLOCK, HeadingBlock


class GenericPageTag(TaggedItemBase):
    content_object = ParentalKey('generic.GenericPage', related_name='tagged_items', on_delete=models.CASCADE)


class GenericPage(BasePage):

    # Page rules.
    template = 'generic_page.html'
    parent_page_types = ['home.HomePage', 'generic.GenericPage', 'help_resources.HelpResourcesMenuItemPage']
    subpage_types = ['generic.GenericPage']
    page_description = 'Make usage of the available blocks and components to build content without restrictions.'

    # Database fields.
    content = StreamField([
        FIXED_LAYOUT_BLOCK,
        FLUID_LAYOUT_BLOCK,
        ('heading', HeadingBlock(group='Page'))
    ], collapsed=True, blank=True, null=True, block_counts={'heading': {'max_num': 1}}, use_json_field=True)
    tags = ClusterTaggableManager(through=GenericPageTag, blank=True)

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

    class Meta:
        verbose_name = 'Generic page'
        verbose_name_plural = 'Generic page'
