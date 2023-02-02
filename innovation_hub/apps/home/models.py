from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core import blocks
from wagtail.fields import StreamField

from innovation_hub.apps.base.models import BasePage
from innovation_hub.apps.case_studies.models import CaseStudiesDetailPage
from innovation_hub.apps.news.models import NewsDetailPage
from innovation_hub.config.blocks import FIXED_LAYOUT_BLOCK, FLUID_LAYOUT_BLOCKS_LIST, HeroBlock


class HomePage(BasePage):

    # Page rules.
    template = 'home_page.html'
    max_count = 1

    # Database fields.
    content = StreamField(
        FIXED_LAYOUT_BLOCK +
        [('fluid', blocks.StructBlock([
            ('background_color', blocks.ChoiceBlock([('default', 'Default'), ('white', 'White')], default='default', required=True)),
            ('content', blocks.StreamBlock(FLUID_LAYOUT_BLOCKS_LIST + [('hero', HeroBlock(group='Components'))], collapsed=True, blank=True, null=True, block_counts={'hero': {'max_num': 1}}, use_json_field=True))
        ], label='Fluid layout', label_format='Fluid layout: {background_color} background', icon='columns-gap'))],
        collapsed=True, blank=True, null=True, use_json_field=True
    )

    # Editor panels configuration.
    content_panels = BasePage.content_panels + [
        FieldPanel('content')
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['news_list'] = NewsDetailPage.objects.live().public().order_by('-first_published_at')[0: 3]
        context['case_studies_list'] = CaseStudiesDetailPage.objects.live().public().order_by('-first_published_at')[0: 3]
        context['last_block_background_color'] = self.content[-1].value['background_color'] if self.content else ''
        return context

    class Meta:
        verbose_name = 'Home page'
        verbose_name_plural = 'Home pages'
