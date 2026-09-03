from django.core.cache import cache
from django.http import HttpResponseBadRequest
from django.http import QueryDict


FILTER_CACHE_TIMEOUT = 60 * 60
MAX_FILTER_VALUES = 10
MAX_FILTER_QUERY_STRING_LENGTH = 2048


def get_valid_filters(path_info):
    """
    Fetch the valid filter values for a list page and cache them for one hour.
    """
    if path_info.startswith("/case-studies/"):
        cache_key = "valid_case_study_filters_v2"
        from is_homepage.apps.case_studies.snippets import CaseStudiesTypeSnippet

        type_model = CaseStudiesTypeSnippet
    elif path_info.startswith("/news/"):
        cache_key = "valid_news_filters_v2"
        from is_homepage.apps.news.snippets import NewsTypeSnippet

        type_model = NewsTypeSnippet
    else:
        return {"types": set(), "tags": set()}

    data = cache.get(cache_key)
    if data is None:
        from taggit.models import Tag

        data = {
            "types": set(type_model.objects.values_list("title", flat=True)),
            "tags": set(Tag.objects.values_list("name", flat=True)),
        }
        cache.set(cache_key, data, FILTER_CACHE_TIMEOUT)

    return data


def _normalise_filter_values(values, valid_values):
    return sorted({value for value in values if value in valid_values})

class SanitizeFiltersMiddleware:
    """
    Globally cleans request query parameters before caching or page rendering:
    1. On index pages (/news/, /case-studies/): Retains only valid filter values 
       and numeric page numbers, stripping everything else.
    2. On all other pages (e.g. homepage /): Strips ALL query parameters completely 
       to prevent botnet cache-busting.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # We only care about GET/HEAD requests that actually contain query parameters
        if request.method in ("GET", "HEAD") and request.path_info.startswith(("/news/", "/case-studies/")):
            query_string = request.META.get("QUERY_STRING", "")
            if len(query_string) > MAX_FILTER_QUERY_STRING_LENGTH:
                return HttpResponseBadRequest("Invalid filter query.")

        if request.method in ("GET", "HEAD") and request.GET:
            cleaned = request.GET.copy()

            # Identify if request is targeting a list page that uses filters
            if request.path_info.startswith(("/news/", "/case-studies/")):
                for key in ("types", "tags"):
                    if len(request.GET.getlist(key)) > MAX_FILTER_VALUES:
                        return HttpResponseBadRequest("Invalid filter query.")

                if any(key in request.GET for key in ("types", "tags")):
                    filters = get_valid_filters(request.path_info)
                else:
                    filters = {"types": set(), "tags": set()}

                # Keep only valid values, with a stable order and no duplicates.
                cleaned = QueryDict("", mutable=True)
                for key in ("types", "tags"):
                    values = _normalise_filter_values(request.GET.getlist(key), filters[key])
                    if values:
                        cleaned.setlist(key, values)

                # Ensure the page parameter is a clean positive integer.
                page = request.GET.get("page")
                if page and page.isdigit() and int(page) > 0:
                    cleaned["page"] = str(int(page))
            else:
                # Strip all query parameters on other pages (e.g. /?random=123)
                cleaned.clear()
                
            # Mutate request object to apply our cleaned/sanitized query parameters
            request.GET = cleaned
            request.META["QUERY_STRING"] = cleaned.urlencode()

        return self.get_response(request)
