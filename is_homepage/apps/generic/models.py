from django.db import models

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey

from taggit.models import TaggedItemBase

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.fields import StreamField

from is_homepage.apps.base.models import BasePage
from is_homepage.config.blocks import FIXED_LAYOUT_BLOCK, FLUID_LAYOUT_BLOCK


class GenericPageTag(TaggedItemBase):
    content_object = ParentalKey('generic.GenericPage', related_name='tagged_items', on_delete=models.CASCADE)


class GenericPage(BasePage):

    # Page rules.
    template = 'generic_page.html'
    parent_page_types = ['home.HomePage']
    subpage_types = []

    # Database fields.
    is_title_visible = models.BooleanField(default=True)

    content = StreamField(FIXED_LAYOUT_BLOCK + FLUID_LAYOUT_BLOCK, collapsed=True, blank=True, null=True, use_json_field=True)

    tags = ClusterTaggableManager(through=GenericPageTag, blank=True)

    # Editor panels configuration.
    content_panels = BasePage.content_panels + [
        FieldPanel('is_title_visible'),
        FieldPanel('content')
    ]
    promote_panels = BasePage.promote_panels + [
        FieldPanel('tags')
    ]

    class Meta:
        verbose_name = 'Generic page'
        verbose_name_plural = 'Generic page'
