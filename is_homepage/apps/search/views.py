from copy import copy

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse

from wagtail.models import Page
from wagtail.search.models import Query

from urllib.parse import urlencode

from is_homepage.apps.case_studies.models import CaseStudiesDetailPage
from is_homepage.apps.generic.models import GenericPage
from is_homepage.apps.generic_navigation.models import GenericNavigationIndexPage, GenericNavigationDetailPage
from is_homepage.apps.innovation_guides.models import InnovationGuidesStagePage, InnovationGuidesDetailPage
from is_homepage.apps.news.models import NewsDetailPage


def search(request):

    pages_types_list = [
        {'name': 'Innovation guides', 'model_type': (InnovationGuidesStagePage, InnovationGuidesDetailPage), 'qp': '', 'is_active': False},
        {'name': 'News', 'model_type': (NewsDetailPage), 'qp': '', 'is_active': False},
        {'name': 'Case studies', 'model_type': (CaseStudiesDetailPage), 'qp': '', 'is_active': False},
        {'name': 'Other', 'model_type': (GenericPage, GenericNavigationIndexPage, GenericNavigationDetailPage), 'qp': '', 'is_active': False}
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

    # Pages filter and search.
    if url_qp_query:

        search_results = Page.objects.live().public().specific()

        pages_types_filter = tuple(value['model_type'] for value in pages_types_list if value['name'] in url_qp_types)
        if len(pages_types_filter) > 0:
            search_results = search_results.type(pages_types_filter)

        search_results = search_results.search(url_qp_query)

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
