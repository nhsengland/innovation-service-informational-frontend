from django.test import TestCase, RequestFactory
from django.core.cache import cache
from unittest.mock import patch
from is_homepage.apps.search.views import search

class SearchViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch('is_homepage.apps.search.views.cache.get')
    def test_search_view_cache_get_exception(self, mock_cache_get):
        # 1. Test that if cache.get() fails, it does not throw 500 error
        mock_cache_get.side_effect = Exception("Cache down")
        request = self.factory.get('/search/?query=innovation')
        response = search(request)
        self.assertEqual(response.status_code, 200)

    def test_search_view_short_query(self):
        # 2. Test short query (<3 characters) returns empty
        request = self.factory.get('/search/?query=in')
        response = search(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['search_results_count'], 0)

    @patch('is_homepage.apps.search.views.cache.get')
    @patch('is_homepage.apps.search.views.Query.get')
    def test_search_view_cache_hit_add_hit(self, mock_query_get, mock_cache_get):
        # 3. Test caching logic and Query.add_hit() call exactly once
        mock_cache_get.return_value = {'results': [], 'count': 0}
        mock_query_instance = mock_query_get.return_value
        
        request = self.factory.get('/search/?query=innovation')
        response = search(request)
        
        self.assertEqual(response.status_code, 200)
        mock_query_instance.add_hit.assert_called_once()
