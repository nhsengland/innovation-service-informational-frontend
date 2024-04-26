from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField

from is_homepage.apps.base.models import BasePage
from is_homepage.apps.generic.models import GenericPage
from is_homepage.apps.generic_navigation.models import GenericNavigationDetailPage, GenericNavigationIndexPage
from is_homepage.config.blocks import FIXED_LAYOUT_BLOCK, FLUID_LAYOUT_BLOCK


class HelpResourcesIndexPage(BasePage):

    # Page rules.
    template = 'help_resources_index_page.html'
    max_count = 1
    parent_page_types = ['home.HomePage']
    subpage_types = ['help_resources.HelpResourcesGroupPage']

    # Database fields.
    content = StreamField([FIXED_LAYOUT_BLOCK, FLUID_LAYOUT_BLOCK], collapsed=True, blank=True, null=True, use_json_field=True)

    # Editor panels configuration.
    content_panels = BasePage.content_panels + [
        FieldPanel('content')
    ]

    def get_context(self, request, *args, **kwargs):

        context = super().get_context(request, *args, **kwargs)

        context['search_params'] = request.GET.get('search', '')

        return context


    class Meta:
        verbose_name = 'Help resources index page'
        verbose_name_plural = 'Help resources index page'


class HelpResourcesGroupPage(GenericNavigationIndexPage):
    """
    This page inherits all behaviours and template from GenericNavigationIndexPage.
    """

    # Page rules.
    template = 'generic_navigation_page.html'
    parent_page_types = ['help_resources.HelpResourcesIndexPage']
    subpage_types = ['help_resources.HelpResourcesMenuItemPage']
    page_description = 'Use this page to group content with a left side menu containing a list of child pages.'
    
    def get_context(self, request, *args, **kwargs):

        context = super().get_context(request, *args, **kwargs)

        context['search_params'] = request.GET.get('search', '')

        return context

    class Meta:
        verbose_name = 'Help resources group page'
        verbose_name_plural = 'Help resources groups page'


class HelpResourcesMenuItemPage(GenericNavigationDetailPage):
    """
    This page inherits all behaviours and template from GenericNavigationDetailPage.
    """

    # Page rules.
    template = 'generic_navigation_page.html'
    parent_page_types = ['help_resources.HelpResourcesGroupPage']
    subpage_types = ['help_resources.HelpResourcesGenericPage']
    page_description = 'This will create and item on the left side menu containing a list of the pages of the same parent.'
    

    class Meta:
        verbose_name = 'Help resources menu item page'
        verbose_name_plural = 'Help resources menu item pages'


class HelpResourcesGenericPage(GenericPage):
    """
    This page inherits all behaviours and template from GenericPage.
    """

    # Page rules.
    template = 'generic_page.html'
    parent_page_types = ['help_resources.HelpResourcesMenuItemPage']
    subpage_types = []

    def get_context(self, request, *args, **kwargs):

        context = super().get_context(request, *args, **kwargs)

        context['search_params'] = request.GET.get('search', '')

        return context

    class Meta:
        verbose_name = 'Help resources detail page'
        verbose_name_plural = 'Help resources detail pages'