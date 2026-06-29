import re
from django.core.cache import cache

def get_valid_filters():
    """
    Fetches the set of all valid category titles (news & case studies) 
    and tags from the database. Caches the result for 1 hour to avoid 
    hitting the database on every request.
    """
    data = cache.get("valid_types_and_tags")
    if not data:
        from is_homepage.apps.case_studies.snippets import CaseStudiesTypeSnippet
        from is_homepage.apps.news.snippets import NewsTypeSnippet
        from taggit.models import Tag
        
        # Combine valid titles from both snippets and tags
        data = {
            "types": set(CaseStudiesTypeSnippet.objects.values_list("title", flat=True)) | \
                     set(NewsTypeSnippet.objects.values_list("title", flat=True)),
            "tags": set(Tag.objects.values_list("name", flat=True))
        }
        cache.set("valid_types_and_tags", data, 3600)  # Cache for 1 hour
    return data

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
        if request.method in ("GET", "HEAD") and request.GET:
            cleaned = request.GET.copy()
            
            # Identify if request is targeting a list page that uses filters
            if request.path_info.startswith(("/news/", "/case-studies/")):
                filters = get_valid_filters()
                
                # Sanitize 'types' and 'tags' parameters
                for key in ("types", "tags"):
                    if key in cleaned:
                        # Retain only values that exist in our database whitelist
                        valid_vals = [v for v in cleaned.getlist(key) if v in filters[key]]
                        cleaned.setlist(key, valid_vals) if valid_vals else cleaned.pop(key, None)
                
                # Ensure the 'page' parameter is a clean positive integer
                if "page" in cleaned and not cleaned.get("page", "").isdigit():
                    cleaned.pop("page", None)
            else:
                # Strip all query parameters on other pages (e.g. /?random=123)
                cleaned.clear()
                
            # Mutate request object to apply our cleaned/sanitized query parameters
            request.GET = cleaned
            request.META["QUERY_STRING"] = cleaned.urlencode()

        return self.get_response(request)
