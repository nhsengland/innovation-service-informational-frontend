from copy import copy

from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.db.models.aggregates import Count

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField

from taggit.models import TaggedItemBase

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.search import index

from is_homepage.apps.base.models import BasePage
from is_homepage.apps.case_studies.snippets import CaseStudiesTypeSnippet
from is_homepage.apps.news.models import NewsDetailPage
from is_homepage.apps.innovation_guides.models import InnovationGuidesDetailPage
from is_homepage.config.blocks import FIXED_LAYOUT_BLOCK, FLUID_LAYOUT_BLOCK


class CaseStudiesDetailPageTag(TaggedItemBase):
    content_object = ParentalKey('case_studies.CaseStudiesDetailPage', related_name='tagged_items', on_delete=models.CASCADE)


class CaseStudiesIndexPage(BasePage):

    # Page rules.
    template = 'case_studies_index_page.html'
    max_count = 1
    parent_page_types = ['home.HomePage']
    subpage_types = ['case_studies.CaseStudiesDetailPage']

    # Database fields.
    content = RichTextField(blank=True)

    # Editor panels configuration.
    content_panels = BasePage.content_panels + [
        FieldPanel('content')
    ]

    def get_context(self, request, *args, **kwargs):

        context = super().get_context(request, *args, **kwargs)

        case_studies_list = CaseStudiesDetailPage.objects.live().public().order_by('-first_published_at')

        case_studies_types_list = list(map(lambda item: {'title': item.title, 'qp': '', 'is_active': False}, CaseStudiesTypeSnippet.objects.all()))

        url_case_studies_types_list = request.GET.getlist('types', None)
        if url_case_studies_types_list:
            case_studies_list = case_studies_list.filter(case_studies_type__title__in=url_case_studies_types_list)

        if request.GET.get('tags', None):
            tags = request.GET.getlist('tags')
            case_studies_list = case_studies_list.filter(tags__name__in=tags)

        # Pagination.
        paginator = Paginator(case_studies_list, 5)
        page = request.GET.get('page')
        try:
            case_studies_list = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            case_studies_list = paginator.page(1)
        except EmptyPage:  # If ?page=x is out of range (too high most likely), return last page.
            page = paginator.num_pages
            case_studies_list = paginator.page(paginator.num_pages)

        # Build news type filter list.
        for item in case_studies_types_list:

            qp = copy(url_case_studies_types_list)

            if item['title'] in url_case_studies_types_list:
                qp.remove(item['title'])
                item['is_active'] = True
            else:
                qp.append(item['title'])
                item['is_active'] = False

            item['qp'] = f"types={'&types='.join(qp)}" if len(qp) > 0 else ''

        context['current_url_query_params'] = f"types={'&types='.join(url_case_studies_types_list)}" if len(url_case_studies_types_list) > 0 else ''
        context['case_studies_types_list'] = case_studies_types_list
        context['case_studies_list'] = case_studies_list
        context['pagination_range'] = case_studies_list.paginator.get_elided_page_range(number=page, on_each_side=1, on_ends=1)
        return context

    class Meta:
        verbose_name = 'Case studies index page'
        verbose_name_plural = 'Case studies index pages'


class CaseStudiesDetailPage(BasePage):

    # Page rules.
    template = 'case_studies_detail_page.html'
    parent_page_types = ['case_studies.CaseStudiesIndexPage']
    subpage_types = []

    # Database fields.
    case_studies_type = ParentalManyToManyField("case_studies.CaseStudiesTypeSnippet", blank=False)

    content = StreamField(FIXED_LAYOUT_BLOCK + FLUID_LAYOUT_BLOCK, collapsed=True, blank=True, null=True, use_json_field=True)

    tags = ClusterTaggableManager(through=CaseStudiesDetailPageTag, blank=True)

    # Editor panels configuration.
    content_panels = BasePage.content_panels + [
        FieldPanel("case_studies_type", widget=forms.CheckboxSelectMultiple),
        FieldPanel('content')
    ]
    promote_panels = BasePage.promote_panels + [
        FieldPanel('tags')
    ]

    # Search index configuration.
    search_fields = BasePage.search_fields + [
        index.RelatedFields('case_studies_type', [index.SearchField('name')]),
        index.RelatedFields('tags', [index.SearchField('name')])
    ]

    def get_context(self, request, *args, **kwargs):

        context = super().get_context(request, *args, **kwargs)

        page_tags = self.tags.all()

        related_content_news = NewsDetailPage.objects.live().public().filter(tags__in=page_tags)
        related_content_news = related_content_news.annotate(Count('title')).exclude(pk=self.pk).order_by('-title__count')[:3]
        related_content_ip = InnovationGuidesDetailPage.objects.live().public().filter(tags__in=page_tags)
        related_content_ip = related_content_ip.annotate(Count('title')).exclude(pk=self.pk).order_by('-title__count')[:3]
        related_content_case_studies = CaseStudiesDetailPage.objects.live().public().filter(tags__in=page_tags)
        related_content_case_studies = related_content_case_studies.annotate(Count('title')).exclude(pk=self.pk).order_by('-title__count')[:3]

        context['related_content_list'] = [related_content_news, related_content_ip, related_content_case_studies]
        context['related_content_count'] = sum([len(items) for items in context['related_content_list']])
        return context

    class Meta:
        verbose_name = 'Case studies detail page'
        verbose_name_plural = 'Case studies detail pages'


CaseStudiesDetailPage._meta.get_field('search_image').blank = False
