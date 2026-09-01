from django.test import SimpleTestCase, RequestFactory
from django.http import HttpResponse
from unittest.mock import patch

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

    def test_disable_media_cache_hook(self):
        # Verify static/media are not cacheable
        req_media = self.factory.get("/media/images/photo.jpg")
        self.assertFalse(disable_media_cache(req_media, True))

        req_health = self.factory.get("/healthz")
        self.assertFalse(disable_media_cache(req_health, True))
        
        req_page = self.factory.get("/")
        self.assertTrue(disable_media_cache(req_page, True))

    @patch("is_homepage.middleware.sanitize_filters.get_valid_filters")
    def test_case_study_filters_are_canonicalized_before_view(self, get_valid_filters):
        get_valid_filters.return_value = {
            "types": {"Type A", "Type B"},
            "tags": set(),
        }
        request = self.factory.get(
            "/case-studies/?types=Type+B&types=Type+A&types=Type+B&unexpected=value&page=001"
        )
        middleware = SanitizeFiltersMiddleware(lambda req: HttpResponse("OK"))

        response = middleware(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.GET.getlist("types"), ["Type A", "Type B"])
        self.assertEqual(request.GET.get("page"), "1")
        self.assertEqual(
            request.META["QUERY_STRING"],
            "types=Type+A&types=Type+B&page=1",
        )
        get_valid_filters.assert_called_once_with("/case-studies/")

    @patch("is_homepage.middleware.sanitize_filters.get_valid_filters")
    def test_rejects_excessive_filter_values_before_allowlist_lookup(self, get_valid_filters):
        request = self.factory.get(
            "/case-studies/?" + "&".join(f"types=Type+{number}" for number in range(11))
        )
        middleware = SanitizeFiltersMiddleware(lambda req: HttpResponse("OK"))

        response = middleware(request)

        self.assertEqual(response.status_code, 400)
        get_valid_filters.assert_not_called()

    @patch("is_homepage.middleware.sanitize_filters.get_valid_filters")
    def test_rejects_oversized_filter_query_before_allowlist_lookup(self, get_valid_filters):
        request = self.factory.get("/case-studies/?types=" + ("x" * 2048))
        middleware = SanitizeFiltersMiddleware(lambda req: HttpResponse("OK"))

        response = middleware(request)

        self.assertEqual(response.status_code, 400)
        get_valid_filters.assert_not_called()


class HealthCheckTests(SimpleTestCase):
    def test_healthz_returns_dependency_free_success_response(self):
        response = self.client.get("/healthz")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "ok"})
        self.assertEqual(
            response["Cache-Control"],
            "no-cache, no-store, max-age=0, private",
        )
