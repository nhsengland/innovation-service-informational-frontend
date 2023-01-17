from django.db import models
from django_extensions.db.fields import AutoSlugField

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel
from wagtail.core.models import Orderable
from wagtail.snippets.models import register_snippet


class MenuItem(Orderable):

    item_title = models.CharField(verbose_name='Title', blank=False, null=True, max_length=50)
    item_description = models.CharField(verbose_name='Description', blank=True, null=True, max_length=500, help_text='Description is only visible within submenus')
    item_url = models.CharField(verbose_name='Url', blank=True, null=True, max_length=255)
    item_page = models.ForeignKey('wagtailcore.Page', verbose_name='Page', null=True, blank=True, related_name='+', on_delete=models.CASCADE)
    open_in_new_tab = models.BooleanField(verbose_name='Open in a new tab?', blank=True, default=False)
    submenu = models.CharField(blank=True, null=True, max_length=50, help_text='Slug of the menu to act as this item submenu')

    menu = ParentalKey('MenuSnippet', related_name='menu_items', help_text='Menu to which this item belongs')

    panels = [
        FieldPanel('item_title'),
        FieldPanel('item_description'),
        FieldPanel('item_url'),
        PageChooserPanel('item_page'),
        FieldPanel('open_in_new_tab'),
        FieldPanel('submenu'),
    ]

    @property
    def title(self):
        if self.item_page and not self.item_title:
            return self.item_page.title
        elif self.item_title:
            return self.item_title
        return 'Missing menu item title'

    @property
    def description(self):
        return self.item_description

    @property
    def link(self):
        if self.item_page:
            return self.item_page.url
        elif self.item_url:
            return self.item_url
        return '#'


@register_snippet
class MenuSnippet(ClusterableModel):

    title = models.CharField(max_length=100)
    slug = AutoSlugField(verbose_name='Identifier', populate_from='title', editable=True, help_text='Unique identifier of menu. Will be populated automatically from title of menu. Change only if needed.')

    panels = [
        MultiFieldPanel([
            FieldPanel('title'),
            FieldPanel('slug')
        ], heading='Menu'),
        InlinePanel('menu_items', label='Menu Item')
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus'
        ordering = ['title']
