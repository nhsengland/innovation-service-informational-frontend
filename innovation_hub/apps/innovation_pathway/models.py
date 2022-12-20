from django.db import models

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page

from wagtailnhsukfrontend.blocks import ActionLinkBlock, CardGroupBlock, InsetTextBlock, RichTextBlock

from innovation_hub.helpers.templates_helper import add_heading_elements_id, heading_elements_ids_list

from innovation_hub.apps.core.snippets import Category


class InnovationPathwayIndexPage(Page):

    template = 'index_page.html'
    max_count = 1
    subpage_types = ['innovation_pathway.InnovationPathwayDetailsPage']

    content = StreamField([
        ('rich_text', RichTextBlock()),
        ('action_link', ActionLinkBlock()),
        ('inset_text', InsetTextBlock()),
        ('card_group', CardGroupBlock())
    ], null=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('content')
    ]

    def get_menu(self):
        children = self.get_children().public().live().specific()
        return list(map(lambda item: {'label': item.title, 'url': item.url}, children))

    class Meta:
        verbose_name = 'Innovation pathway index page'
        verbose_name_plural = 'Innovation pathway index page'


class InnovationPathwayDetailsPage(Page):

    template = 'details_page.html'
    subpage_types = []

    category = models.ForeignKey(
        Category,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+')

    content = StreamField([
        ('rich_text', RichTextBlock()),
        ('inset_text', InsetTextBlock()),
        ('card_group', CardGroupBlock())
    ], null=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('category'),
        FieldPanel('content')
    ]

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
        verbose_name_plural = 'Innovation pathway details page'
