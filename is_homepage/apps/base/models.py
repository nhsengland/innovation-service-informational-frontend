from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator

from django_ratelimit.decorators import ratelimit

from wagtail.admin.panels import FieldPanel
from wagtail.models import Page
from wagtailmetadata.models import MetadataPageMixin


class BasePage(MetadataPageMixin, Page):

    # Editor panels configuration.
    promote_panels = [
        FieldPanel('slug'),
        FieldPanel('seo_title'),
        # FieldPanel('show_in_menus'),
        FieldPanel('search_description'),
        FieldPanel('search_image')
    ]

    def full_clean(self, *args, **kwargs):
        """Override validation making 'search_description' field required."""

        errors = {}

        if not self.search_description:
            errors['search_description'] = 'This field is required'

        if errors:
            raise ValidationError(errors)

    @method_decorator(ratelimit(key='ip', rate='5/s', block=True), name='serve')
    @method_decorator(ratelimit(key='ip', rate='10/m', block=True), name='serve')
    @method_decorator(ratelimit(key='ip', rate='1000/h', block=True), name='serve')
    @method_decorator(ratelimit(key='ip', rate='10000/d', block=True), name='serve')
    def serve(self, request, *args, **kwargs):
        return super().serve(request, *args, **kwargs)

    class Meta:
        abstract = True


BasePage._meta.get_field('seo_title').verbose_name = 'Search title'
BasePage._meta.get_field('search_description').verbose_name = 'Search description'
