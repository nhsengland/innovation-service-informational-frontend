import copy

from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.shortcuts import render

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager

from wagtail.core.fields import RichTextField, StreamField

from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route, path
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.blocks import ImageChooserBlock

from wagtailnhsukfrontend.blocks import ActionLinkBlock, CardGroupBlock, InsetTextBlock, RichTextBlock

# from wagtail.images.edit_handlers import ImageChooserPanel

# from wagtail.snippets.edit_handlers import SnippetChooserPanel
# from wagtail.core.fields import StreamField
# from wagtail.core.models import Page, Orderable
# from wagtail.images.edit_handlers import ImageChooserPanel
# from wagtail.images.api.fields import ImageRenditionField
# from wagtail.snippets.models import register_snippet

# from streams import blocks


from innovation_hub.apps.news.snippets import NewsTypeSnippet


class NewsListPage(RoutablePageMixin, Page):

    template = 'list_page.html'
    max_count = 1
    parent_page_types = ['home.HomePage']
    subpage_types = ['news.NewsDetailPage']

    content = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('content')
    ]

    def get_context(self, request, *args, **kwargs):

        context = super().get_context(request, *args, **kwargs)

        news_list = NewsDetailPage.objects.live().public().order_by('-first_published_at')

        url_news_types_list = request.GET.getlist('types', None)
        news_types_filter_list = list(map(lambda item: {'name': item.name, 'qp': '', 'is_active': False}, NewsTypeSnippet.objects.all()))

        if url_news_types_list:
            news_list = news_list.filter(news_type__name__in=url_news_types_list)

        # Paginator
        paginator = Paginator(news_list, 2)
        page = request.GET.get('page')
        try:
            news_list = paginator.page(page)
        except PageNotAnInteger:
            news_list = paginator.page(1)
        except EmptyPage:  # If ?page=x is out of range (too high most likely), return last page.
            news_list = paginator.page(paginator.num_pages)

        # Build news type filter list.
        for item in news_types_filter_list:

            qp = copy.copy(url_news_types_list)

            if item['name'] in url_news_types_list:
                qp.remove(item['name'])
                item['is_active'] = True
            else:
                qp.append(item['name'])
                item['is_active'] = False

            item['qp'] = f"types={'&types='.join(qp)}" if len(qp) > 0 else ''

        context['current_url_query_params'] = f"types={'&types='.join(url_news_types_list)}" if len(url_news_types_list) > 0 else ''
        context['news_types_filter_list'] = news_types_filter_list
        context['news_list'] = news_list
        return context

    def get_child_pages(self):
        return self.get_children().live().public()
        # return self.get_children().public().live().values("id", "title", "slug")

    # Concept case, if we need news by year/month.
    @route(r"^year/(\d{4})/?(\d{1,2})?/?$", name="news_by_year_month")
    def news_by_year_month(self, request, year=None, month=None):

        context = self.get_context(request)
        news_list = context['news_list'].filter(first_published_at__year=year)

        if month is not None:
            news_list = news_list.filter(first_published_at__month=month)

        context['news_list'] = news_list

        return render(request, self.template, context)

    class Meta:
        verbose_name = 'News list page'
        verbose_name_plural = 'News list page'


class NewsDetailPage(Page):

    template = 'detail_page.html'
    parent_page_types = ['news.NewsListPage']
    subpage_types = []

    news_image = models.ForeignKey('wagtailimages.Image', blank=True, null=True, related_name="+", on_delete=models.SET_NULL)

    summary = models.CharField(max_length=100, blank=False, null=True)

    news_type = ParentalManyToManyField("news.NewsTypeSnippet", blank=False)

    content = StreamField([
        ('rich_text', RichTextBlock()),
        ('inset_text', InsetTextBlock()),
        ('card_group', CardGroupBlock()),
        # ('image_chooser', ImageChooserBlock())
    ], null=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('summary'),
        FieldPanel("news_image"),
        FieldPanel("news_type", widget=forms.CheckboxSelectMultiple),
        FieldPanel('content')
    ]

    # def previous_sibling(self):
    #     return self.get_prev_sibling()

    # def next_sibling(self):
    #     return self.get_next_sibling()

    class Meta:
        verbose_name = 'News detail page'
        verbose_name_plural = 'News detail page'
