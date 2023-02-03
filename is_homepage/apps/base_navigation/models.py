from django.db import models
from django_extensions.db.fields import AutoSlugField

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel
from wagtail.core.models import Orderable
from wagtail.snippets.models import register_snippet


@register_snippet
class BaseNavigationSnippet(ClusterableModel):

    title = models.CharField(max_length=100)
    slug = AutoSlugField(verbose_name='Menu identifier', populate_from='title', editable=True, help_text='Unique identifier of the menu.')

    panels = [
        MultiFieldPanel([
            FieldPanel('title'),
            FieldPanel('slug')
        ], heading='Menu'),
        InlinePanel('navigation_menu_items', label='Menu Item')
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Navigation'
        verbose_name_plural = 'Navigation'
        ordering = ['title']


class NavigationMenuItem(Orderable):

    menu_title = models.CharField(verbose_name='Title', blank=False, null=True, max_length=50)
    menu_description = models.CharField(verbose_name='Description', blank=True, null=True, max_length=500, help_text='Description is only visible within submenus')
    menu_url = models.CharField(verbose_name='Url', blank=True, null=True, max_length=255)
    menu_page = models.ForeignKey('wagtailcore.Page', verbose_name='Page', null=True, blank=True, related_name='+', on_delete=models.CASCADE)
    open_in_new_tab = models.BooleanField(verbose_name='Open in a new tab?', blank=True, default=False)
    submenu = models.CharField(blank=True, null=True, max_length=50, help_text='Slug of the menu to act as this item submenu')

    menu = ParentalKey(BaseNavigationSnippet, related_name='navigation_menu_items', help_text='Menu to which this item belongs')

    panels = [
        FieldPanel('menu_title'),
        FieldPanel('menu_description'),
        FieldPanel('menu_url'),
        PageChooserPanel('menu_page'),
        FieldPanel('open_in_new_tab'),
        FieldPanel('submenu')
    ]

    @property
    def title(self):
        if self.menu_page and not self.menu_title:
            return self.menu_page.title
        elif self.menu_title:
            return self.menu_title
        return 'Missing menu item title'

    @property
    def description(self):
        return self.menu_description

    @property
    def link(self):
        if self.menu_page:
            return self.menu_page.url
        elif self.menu_url:
            return self.menu_url
        return '#'
