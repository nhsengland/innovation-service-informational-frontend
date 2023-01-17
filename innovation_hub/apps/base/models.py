from wagtail.admin.edit_handlers import FieldPanel
from wagtail.models import Page

from wagtailmetadata.models import MetadataPageMixin


class BasePage(MetadataPageMixin, Page):

    # Editor panels configuration.
    promote_panels = [
        FieldPanel('slug'),
        FieldPanel('seo_title'),
        # FieldPanel('show_in_menus'),
        FieldPanel('search_description'),
        FieldPanel('search_image'),
    ]

    class Meta:
        abstract = True


# Default fields overwrites.
BasePage._meta.get_field('seo_title').verbose_name = 'Search title'
BasePage._meta.get_field('search_description').blank = False
BasePage._meta.get_field('search_description').verbose_name = 'Search description'
