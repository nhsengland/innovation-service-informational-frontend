from copy import copy

from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.db.models.aggregates import Count
from django.shortcuts import render

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField

from taggit.models import TaggedItemBase

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.fields import RichTextField, StreamField
from wagtail.search import index

from innovation_hub.apps.base.models import BasePage
from innovation_hub.apps.news.snippets import NewsTypeSnippet
from innovation_hub.config.blocks.stream_field_blocks import BLOCKS_BASE_LIST


class NewsDetailPageTag(TaggedItemBase):
    content_object = ParentalKey('news.NewsDetailPage', related_name='tagged_items', on_delete=models.CASCADE)


class NewsIndexPage(RoutablePageMixin, BasePage):

    # Page rules.
    template = 'news_index_page.html'
    max_count = 1
    parent_page_types = ['home.HomePage']
    subpage_types = ['news.NewsDetailPage']

    # Database fields.
    content = RichTextField(blank=True)

    # Editor panels configuration.
    content_panels = BasePage.content_panels + [
        FieldPanel('content')
    ]

    def get_context(self, request, *args, **kwargs):

        context = super().get_context(request, *args, **kwargs)

        news_list = NewsDetailPage.objects.live().public().order_by('-first_published_at')

        news_types_list = list(map(lambda item: {'name': item.name, 'qp': '', 'is_active': False}, NewsTypeSnippet.objects.all()))

        url_news_types_list = request.GET.getlist('types', None)
        if url_news_types_list:
            news_list = news_list.filter(news_type__name__in=url_news_types_list)

        if request.GET.get('tags', None):
            tags = request.GET.getlist('tags')
            news_list = news_list.filter(tags__name__in=tags)

        # Pagination.
        paginator = Paginator(news_list, 5)
        page = request.GET.get('page')
        try:
            news_list = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            news_list = paginator.page(1)
        except EmptyPage:  # If ?page=x is out of range (too high most likely), return last page.
            page = paginator.num_pages
            news_list = paginator.page(paginator.num_pages)

        # Build news type filter list.
        for item in news_types_list:

            qp = copy(url_news_types_list)

            if item['name'] in url_news_types_list:
                qp.remove(item['name'])
                item['is_active'] = True
            else:
                qp.append(item['name'])
                item['is_active'] = False

            item['qp'] = f"types={'&types='.join(qp)}" if len(qp) > 0 else ''

        context['current_url_query_params'] = f"types={'&types='.join(url_news_types_list)}" if len(url_news_types_list) > 0 else ''
        context['news_types_list'] = news_types_list
        context['news_list'] = news_list
        context['pagination_range'] = news_list.paginator.get_elided_page_range(number=page, on_each_side=1, on_ends=1)
        return context

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
        verbose_name = 'News index page'
        verbose_name_plural = 'News index pages'


class NewsDetailPage(BasePage):

    # Page rules.
    template = 'news_detail_page.html'
    parent_page_types = ['news.NewsIndexPage']
    subpage_types = []

    # Database fields.
    news_type = ParentalManyToManyField("news.NewsTypeSnippet", blank=False)

    content = StreamField(BLOCKS_BASE_LIST, collapsed=True, null=True, use_json_field=True)

    tags = ClusterTaggableManager(through=NewsDetailPageTag, blank=True)

    # Editor panels configuration.
    content_panels = BasePage.content_panels + [
        FieldPanel("news_type", widget=forms.CheckboxSelectMultiple),
        FieldPanel('content')
    ]
    promote_panels = BasePage.promote_panels + [
        FieldPanel('tags')
    ]

    # Search index configuration.
    search_fields = BasePage.search_fields + [
        index.RelatedFields('news_type', [index.SearchField('name')]),
        index.RelatedFields('tags', [index.SearchField('name')])
    ]

    def get_context(self, request, *args, **kwargs):

        context = super().get_context(request, *args, **kwargs)

        page_tags = self.tags.all()

        related_content_news = NewsDetailPage.objects.live().public().filter(tags__in=page_tags)
        related_content_news = related_content_news.annotate(Count('title')).exclude(pk=self.pk).order_by('-title__count')[:3]

        context['related_content_list'] = [related_content_news]
        return context

    class Meta:
        verbose_name = 'News detail page'
        verbose_name_plural = 'News detail pages'
