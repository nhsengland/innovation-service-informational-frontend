import re
from django.core.cache import cache

def get_valid_filters():
    data = cache.get("valid_types_and_tags")
    if not data:
        from is_homepage.apps.case_studies.snippets import CaseStudiesTypeSnippet
        from is_homepage.apps.news.snippets import NewsTypeSnippet
        from taggit.models import Tag
        
        valid_types = set(CaseStudiesTypeSnippet.objects.values_list("title", flat=True)) | \
                      set(NewsTypeSnippet.objects.values_list("title", flat=True))
        valid_tags = set(Tag.objects.values_list("name", flat=True))
        
        data = {"types": valid_types, "tags": valid_tags}
        cache.set("valid_types_and_tags", data, 3600)  # Cache for 1 hour
    return data

class SanitizeFiltersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info
        is_index_page = path.startswith(("/news/", "/case-studies/"))
        
        if request.method in ("GET", "HEAD") and len(request.GET) > 0:
            # Make mutable copy of GET parameters
            cleaned_get = request.GET.copy()
            
            if is_index_page:
                valid_filters = get_valid_filters()
                
                # 1. Clean 'types'
                if "types" in cleaned_get:
                    valid_types_submitted = [
                        t for t in cleaned_get.getlist("types")
                        if t in valid_filters["types"]
                    ]
                    if valid_types_submitted:
                        cleaned_get.setlist("types", valid_types_submitted)
                    else:
                        cleaned_get.pop("types", None)
                        
                # 2. Clean 'tags'
                if "tags" in cleaned_get:
                    valid_tags_submitted = [
                        t for t in cleaned_get.getlist("tags")
                        if t in valid_filters["tags"]
                    ]
                    if valid_tags_submitted:
                        cleaned_get.setlist("tags", valid_tags_submitted)
                    else:
                        cleaned_get.pop("tags", None)
                        
                # 3. Clean 'page' (must be integer)
                if "page" in cleaned_get:
                    page_val = cleaned_get.get("page")
                    if not page_val.isdigit():
                        cleaned_get.pop("page", None)
            else:
                # Strip ALL query parameters on other pages (e.g. / with ?types=val)
                cleaned_get.clear()
            
            request.GET = cleaned_get
            request.META["QUERY_STRING"] = cleaned_get.urlencode()

        return self.get_response(request)
