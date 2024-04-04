from copy import copy
from itertools import chain

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse

from wagtail.documents.models import Document
from wagtail.models import Page
from wagtail.contrib.search_promotions.models import Query

from urllib.parse import urlencode

from wagtail.search.backends.elasticsearch8 import (Elasticsearch8SearchQueryCompiler)

from is_homepage.apps.case_studies.models import CaseStudiesDetailPage
from is_homepage.apps.generic.models import GenericPage
from is_homepage.apps.generic_navigation.models import GenericNavigationIndexPage, GenericNavigationDetailPage
from is_homepage.apps.innovation_guides.models import InnovationGuidesIndexPage, InnovationGuidesStagePage, InnovationGuidesDetailPage
from is_homepage.apps.news.models import NewsDetailPage
from is_homepage.apps.help_resources.models import HelpResourcesGenericPage, HelpResourcesGroupPage, HelpResourcesIndexPage, HelpResourcesMenuItemPage
from is_homepage.config.helpers.iterables_helper import flatten_tuple


def search(request):

    pages_types_list = [
        {'name': 'Innovation guides', 'model_type': 'page', 'models': (InnovationGuidesIndexPage, InnovationGuidesStagePage, InnovationGuidesDetailPage), 'qp': '', 'is_active': False},
        {'name': 'News', 'model_type': 'page', 'models': (NewsDetailPage), 'qp': '', 'is_active': False},
        {'name': 'Case studies', 'model_type': 'page', 'models': (CaseStudiesDetailPage), 'qp': '', 'is_active': False},
        {'name': 'Help and resources', 'model_type': 'page', 'models': (HelpResourcesIndexPage, HelpResourcesGroupPage, HelpResourcesMenuItemPage, HelpResourcesGenericPage), 'qp': '', 'is_active': False},
        {'name': 'Documents', 'model_type': 'document', 'models': (Document), 'qp': '', 'is_active': False},
        {'name': 'Other', 'model_type': 'page', 'models': (GenericPage, GenericNavigationIndexPage, GenericNavigationDetailPage), 'qp': '', 'is_active': False},
    ]

    url_qp_query = request.GET.get('query', None)
    url_qp_types = request.GET.getlist('types', None)

    current_url_qp = urlencode(({key: value for (key, value) in {
        'query': url_qp_query if url_qp_query else None,
        'types': url_qp_types if url_qp_types else None
    }.items() if value}), True)

    # Build page types filter list.
    for item in pages_types_list:

        qp = copy(url_qp_types)

        if item['name'] in url_qp_types:
            qp.remove(item['name'])
            item['is_active'] = True
        else:
            qp.append(item['name'])
            item['is_active'] = False

        item['qp'] = urlencode(({key: value for (key, value) in {
            'query': url_qp_query if url_qp_query else None,
            'types': qp if len(qp) > 0 else None
        }.items() if value}), True)

    # Models filter and search.
    if url_qp_query:

        pages = None
        documents = None
        promoted = None

        page_types_filter = tuple(value['models'] for value in pages_types_list if value['model_type'] == 'page' and value['name'] in url_qp_types)
        page_types_filter = flatten_tuple(page_types_filter)
        document_types_filter = tuple(value['models'] for value in pages_types_list if value['model_type'] == 'document' and value['name'] in url_qp_types)
        document_types_filter = flatten_tuple(document_types_filter)

        if len(page_types_filter) == 0 and len(document_types_filter) == 0:
            # No filters applied, return everything.
            pages = Page.objects.live().public().specific()
            documents = Document.objects
            promoted = list(value.page.get_specific(deferred=True) for value in Query.get(url_qp_query).editors_picks.all())
        else:

            if len(page_types_filter) > 0:
                pages = Page.objects.live().public().specific().type(page_types_filter)
                promoted = list(value.page.get_specific(deferred=True) for value in Query.get(url_qp_query).editors_picks.all())
                promoted = list(value for value in promoted if value.__class__ in page_types_filter)

            if len(document_types_filter) > 0:
                documents = Document.objects

        # Adds a "high" '_score' promoted search (as it don't have it) so that it can be sortable just like the other datasets.
        if promoted:
            for value in promoted:
                value._score = 0.8

        # As we are joining different models, we need to bring the models score (annotate_score) so that dataset could be ordered after.
        Elasticsearch8SearchQueryCompiler
        search_results = list(chain(
            pages.search(url_qp_query).annotate_score('_score') if pages else [],
            documents.search(url_qp_query).annotate_score('_score') if documents else [],
            promoted if promoted else []
        ))
        search_results.sort(key=lambda x: x._score, reverse=True)

        # This code is just for debugging purposes. Shows the dataset results with the score.
        # for event in search_results:
        #     print(event.title, event._score)

        query = Query.get(url_qp_query)
        query.add_hit()  # Record hit

    else:
        search_results = Page.objects.none()

    # Pagination.
    paginator = Paginator(search_results, 5)
    page = request.GET.get('page', 1)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        search_results = paginator.page(1)
    except EmptyPage:
        page = paginator.num_pages
        search_results = paginator.page(paginator.num_pages)

    return TemplateResponse(request, 'search/search.html', {
        'search_query': url_qp_query,
        'search_results': search_results,
        'pages_types_list': pages_types_list,
        'current_url_query_params': current_url_qp,
        'pagination_range': search_results.paginator.get_elided_page_range(number=page, on_each_side=2, on_ends=1)
    })
