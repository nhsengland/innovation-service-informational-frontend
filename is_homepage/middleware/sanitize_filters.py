import re
from django.core.cache import cache

def get_valid_filters():
    data = cache.get("valid_types_and_tags")
    if not data:
        from is_homepage.apps.case_studies.snippets import CaseStudiesTypeSnippet
        from is_homepage.apps.news.snippets import NewsTypeSnippet
        from taggit.models import Tag
        
        data = {
            "types": set(CaseStudiesTypeSnippet.objects.values_list("title", flat=True)) | \
                     set(NewsTypeSnippet.objects.values_list("title", flat=True)),
            "tags": set(Tag.objects.values_list("name", flat=True))
        }
        cache.set("valid_types_and_tags", data, 3600)  # Cache for 1 hour
    return data

class SanitizeFiltersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in ("GET", "HEAD") and request.GET:
            cleaned = request.GET.copy()
            
            if request.path_info.startswith(("/news/", "/case-studies/")):
                filters = get_valid_filters()
                for key in ("types", "tags"):
                    if key in cleaned:
                        valid_vals = [v for v in cleaned.getlist(key) if v in filters[key]]
                        cleaned.setlist(key, valid_vals) if valid_vals else cleaned.pop(key, None)
                
                if "page" in cleaned and not cleaned.get("page", "").isdigit():
                    cleaned.pop("page", None)
            else:
                cleaned.clear()
                
            request.GET = cleaned
            request.META["QUERY_STRING"] = cleaned.urlencode()

        return self.get_response(request)
