from django.test import SimpleTestCase, RequestFactory
from django.http import HttpResponse
from is_homepage.middleware.sanitize_filters import SanitizeFiltersMiddleware
from is_homepage.apps.base.wagtail_hooks import disable_media_cache

class CacheSanitizationTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_sanitize_filters_middleware_homepage(self):
        # Query params should be stripped completely on the homepage
        request = self.factory.get("/?types=invalid&random=123")
        middleware = SanitizeFiltersMiddleware(lambda req: HttpResponse("OK"))
        middleware(request)
        self.assertEqual(len(request.GET), 0)
        self.assertEqual(request.META["QUERY_STRING"], "")

    def test_sanitize_filters_middleware_search_preserves_search_params(self):
        request = self.factory.get(
            "/search/?query=innovation&types=News&page=2&random=123"
        )
        middleware = SanitizeFiltersMiddleware(lambda req: HttpResponse("OK"))
        middleware(request)
        self.assertEqual(request.GET.get("query"), "innovation")
        self.assertEqual(request.GET.getlist("types"), ["News"])
        self.assertEqual(request.GET.get("page"), "2")
        self.assertNotIn("random", request.GET)

    def test_disable_media_cache_hook(self):
        # Verify static/media are not cacheable
        req_media = self.factory.get("/media/images/photo.jpg")
        self.assertFalse(disable_media_cache(req_media, True))

        req_search = self.factory.get("/search/?query=innovation")
        self.assertFalse(disable_media_cache(req_search, True))
        
        req_page = self.factory.get("/")
        self.assertTrue(disable_media_cache(req_page, True))
