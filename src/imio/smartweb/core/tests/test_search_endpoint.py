# -*- coding: utf-8 -*-

from imio.smartweb.core import config
from imio.smartweb.core.contents.rest.search.endpoint import _cache_key
from imio.smartweb.core.contents.rest.search.endpoint import ExtendedSearchHandler
from imio.smartweb.core.contents.rest.search.endpoint import get_default_view_url
from imio.smartweb.core.contents.rest.search.endpoint import get_events_views
from imio.smartweb.core.contents.rest.search.endpoint import get_navigation_root
from imio.smartweb.core.contents.rest.search.endpoint import get_news_views
from imio.smartweb.core.contents.rest.search.endpoint import get_views_mapping
from imio.smartweb.core.contents.rest.search.endpoint import SearchGet
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.restapi.search.handler import SearchHandler
from plone.uuid.interfaces import IUUID
from unittest.mock import MagicMock
from unittest.mock import patch
from zope.component import queryMultiAdapter


class TestSearchEndpointHelpers(ImioSmartwebTestCase):
    """Tests for helper functions in search/endpoint.py"""

    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_cache_key_with_uid(self):
        key = _cache_key(None, self.portal)
        self.assertIsInstance(key, tuple)
        self.assertEqual(len(key), 2)
        self.assertNotEqual(key[0], "PloneSite")

    def test_cache_key_without_uid(self):
        class NoUID:
            pass

        key = _cache_key(None, NoUID())
        self.assertEqual(key[0], "PloneSite")

    def test_get_news_views_empty(self):
        views = get_news_views(self.portal)
        self.assertIsInstance(views, dict)

    def test_get_events_views_empty(self):
        views = get_events_views(self.portal)
        self.assertIsInstance(views, dict)

    def test_get_navigation_root_is_navigation_root(self):
        result = get_navigation_root(self.portal)
        self.assertEqual(result, self.portal)

    def test_get_navigation_root_traverses_chain(self):
        page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            id="test-nav-page",
        )
        result = get_navigation_root(page)
        self.assertEqual(result, self.portal)

    def test_get_default_view_url_not_set(self):
        result = get_default_view_url("events")
        self.assertEqual(result, "")

    def test_get_default_view_url_uid_not_found(self):
        with patch(
            "imio.smartweb.core.contents.rest.search.endpoint.api.portal.get_registry_record",
            return_value="00000000000000000000000000000099",
        ):
            result = get_default_view_url("events")
            self.assertEqual(result, "")

    def test_get_default_view_url_with_valid_uid(self):
        events_view = api.content.create(
            container=self.portal,
            type="imio.smartweb.EventsView",
            id="test-events-view",
        )
        uid = IUUID(events_view)
        with patch(
            "imio.smartweb.core.contents.rest.search.endpoint.api.portal.get_registry_record",
            return_value=uid,
        ):
            result = get_default_view_url("events")
            self.assertEqual(result, events_view.absolute_url())

    def test_get_views_mapping_structure(self):
        mapping = get_views_mapping(self.portal)
        self.assertIn("imio.news.NewsItem", mapping)
        self.assertIn("imio.events.Event", mapping)
        self.assertIn("imio.directory.Contact", mapping)
        self.assertIn("default", mapping["imio.news.NewsItem"])
        self.assertIn("default", mapping["imio.events.Event"])
        self.assertIn("default", mapping["imio.directory.Contact"])


class TestExtendedSearchHandler(ImioSmartwebTestCase):
    """Tests for ExtendedSearchHandler methods"""

    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_navigation_root_property(self):
        page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            id="test-search-page",
        )
        handler = ExtendedSearchHandler(page, self.request)
        self.assertEqual(handler._navigation_root, self.portal)

    def test_update_metadata_fields_string_original(self):
        handler = ExtendedSearchHandler(self.portal, self.request)
        result = handler._update_metadata_fields(
            "existing_field", ["new_field", "existing_field"]
        )
        self.assertIn("existing_field", result)
        self.assertIn("new_field", result)
        self.assertEqual(result.count("existing_field"), 1)

    def test_update_metadata_fields_list_original(self):
        handler = ExtendedSearchHandler(self.portal, self.request)
        result = handler._update_metadata_fields(
            ["field1", "field2"], ["field2", "field3"]
        )
        self.assertIn("field1", result)
        self.assertIn("field2", result)
        self.assertIn("field3", result)
        self.assertEqual(result.count("field2"), 1)

    def test_get_source_url_news(self):
        handler = ExtendedSearchHandler(self.portal, self.request)
        url = handler._get_source_url("/plone/news/item", "news")
        self.assertIn(config.NEWS_URL, url)
        self.assertIn("news/item", url)

    def test_get_source_url_events(self):
        handler = ExtendedSearchHandler(self.portal, self.request)
        url = handler._get_source_url("/plone/events/item", "events")
        self.assertIn(config.EVENTS_URL, url)

    def test_get_source_url_directory(self):
        handler = ExtendedSearchHandler(self.portal, self.request)
        url = handler._get_source_url("/plone/directory/contact", "directory")
        self.assertIn(config.DIRECTORY_URL, url)

    def test_get_source_url_unknown_core(self):
        handler = ExtendedSearchHandler(self.portal, self.request)
        url = handler._get_source_url("/plone/content/item", "unknown")
        self.assertIn("content/item", url)

    def test_core_query_news(self):
        handler = ExtendedSearchHandler(self.portal, self.request)
        params = handler._core_query("news")
        self.assertIsNotNone(params)
        self.assertEqual(params["portal_type"], ["imio.news.NewsItem"])
        self.assertIn("selected_news_folders", params)

    def test_core_query_events(self):
        handler = ExtendedSearchHandler(self.portal, self.request)
        params = handler._core_query("events")
        self.assertIsNotNone(params)
        self.assertEqual(params["portal_type"], ["imio.events.Event"])
        self.assertIn("selected_agendas", params)

    def test_core_query_directory(self):
        handler = ExtendedSearchHandler(self.portal, self.request)
        params = handler._core_query("directory")
        self.assertIsNotNone(params)
        self.assertEqual(params["portal_type"], ["imio.directory.Contact"])
        self.assertIn("selected_entities", params)

    def test_core_query_unknown_returns_none(self):
        handler = ExtendedSearchHandler(self.portal, self.request)
        params = handler._core_query("unknown")
        self.assertIsNone(params)

    def test_core_query_with_non_fr_language_adds_translated_fields(self):
        handler = ExtendedSearchHandler(self.portal, self.request)
        params = handler._core_query("news", language="nl")
        self.assertIn("title_nl", params["metadata_fields"])
        self.assertIn("description_nl", params["metadata_fields"])
        self.assertTrue(params.get("translated_in_nl"))

    def test_adapt_result_values_unknown_type_passthrough(self):
        handler = ExtendedSearchHandler(self.portal, self.request)
        item = {"@type": "unknown.Type", "UID": "uid"}
        mapping = {"imio.news.NewsItem": {"default": ""}}
        result = handler._adapt_result_values(item, mapping, "news")
        self.assertEqual(result, item)

    def test_adapt_result_values_known_type_adds_urls(self):
        handler = ExtendedSearchHandler(self.portal, self.request)
        item = {
            "@type": "imio.news.NewsItem",
            "container_uid": "some-uid",
            "UID": "item-uid",
            "path_string": "/plone/news/item",
            "modified": "2021-09-14T08:00:00",
        }
        mapping = {"imio.news.NewsItem": {"default": "http://nohost/plone/news-view"}}
        result = handler._adapt_result_values(item, mapping, "news")
        self.assertIn("_url", result)
        self.assertIn("item-uid", result["_url"])
        self.assertIn("_source_url", result)
        self.assertIn("image_url", result)

    def test_adapt_result_values_uses_container_uid_when_matched(self):
        handler = ExtendedSearchHandler(self.portal, self.request)
        item = {
            "@type": "imio.news.NewsItem",
            "container_uid": "folder-uid",
            "UID": "item-uid",
            "path_string": "/plone/news/item",
            "modified": "2021-09-14T08:00:00",
        }
        mapping = {
            "imio.news.NewsItem": {
                "folder-uid": "http://nohost/plone/specific-view",
                "default": "http://nohost/plone/default-view",
            }
        }
        result = handler._adapt_result_values(item, mapping, "news")
        self.assertIn("specific-view", result["_url"])

    def test_adapt_result_values_translates_fields_for_non_fr_language(self):
        handler = ExtendedSearchHandler(self.portal, self.request)
        item = {
            "@type": "imio.news.NewsItem",
            "container_uid": "some-uid",
            "UID": "item-uid",
            "path_string": "/plone/news/item",
            "modified": "2021-09-14T08:00:00",
            "title_nl": "Dutch title",
            "description_nl": "Dutch description",
        }
        mapping = {"imio.news.NewsItem": {"default": "http://nohost/plone/news-view"}}
        result = handler._adapt_result_values(item, mapping, "news", language="nl")
        self.assertEqual(result["title"], "Dutch title")
        self.assertEqual(result["description"], "Dutch description")
        self.assertNotIn("title_nl", result)
        self.assertNotIn("description_nl", result)

    def test_adapt_result_loops_items(self):
        handler = ExtendedSearchHandler(self.portal, self.request)
        mock_result = {
            "items": [
                {
                    "@type": "imio.news.NewsItem",
                    "container_uid": "some-uid",
                    "UID": "item-uid",
                    "path_string": "/plone/news/item",
                    "modified": "2021-09-14T08:00:00",
                }
            ],
            "items_total": 1,
        }
        result = handler._adapt_result(mock_result, "news")
        self.assertEqual(len(result["items"]), 1)
        self.assertIn("_url", result["items"][0])

    def test_adapt_result_empty_items(self):
        handler = ExtendedSearchHandler(self.portal, self.request)
        mock_result = {"items": [], "items_total": 0}
        result = handler._adapt_result(mock_result, "news")
        self.assertEqual(result["items"], [])

    def test_search_basic_no_core(self):
        mock_result = {
            "items": [],
            "items_total": 0,
            "@id": "http://nohost/plone/@search",
        }
        with patch.object(SearchHandler, "search", return_value=mock_result):
            handler = ExtendedSearchHandler(self.portal, self.request)
            result = handler.search({"SearchableText": "test"})
            self.assertEqual(result, mock_result)

    def test_search_with_existing_use_site_search_settings(self):
        mock_result = {"items": [], "items_total": 0}
        with patch.object(SearchHandler, "search", return_value=mock_result):
            handler = ExtendedSearchHandler(self.portal, self.request)
            result = handler.search({"use_site_search_settings": True})
            self.assertEqual(result, mock_result)

    def test_search_with_existing_use_solr_false(self):
        mock_result = {"items": [], "items_total": 0}
        with patch.object(SearchHandler, "search", return_value=mock_result):
            handler = ExtendedSearchHandler(self.portal, self.request)
            result = handler.search({"use_solr": False})
            self.assertEqual(result, mock_result)

    def test_search_with_core_news(self):
        mock_result = {"items": [], "items_total": 0}
        with patch.object(SearchHandler, "search", return_value=mock_result):
            handler = ExtendedSearchHandler(self.portal, self.request)
            result = handler.search({"_core": "news"})
            self.assertIsNotNone(result)

    def test_search_with_core_events(self):
        mock_result = {"items": [], "items_total": 0}
        with patch.object(SearchHandler, "search", return_value=mock_result):
            handler = ExtendedSearchHandler(self.portal, self.request)
            result = handler.search({"_core": "events"})
            self.assertIsNotNone(result)

    def test_search_with_core_and_metadata_fields(self):
        mock_result = {"items": [], "items_total": 0}
        with patch.object(SearchHandler, "search", return_value=mock_result):
            handler = ExtendedSearchHandler(self.portal, self.request)
            result = handler.search({"_core": "news", "metadata_fields": ["my_field"]})
            self.assertIsNotNone(result)

    def test_search_with_core_non_fr_language_and_searchable_text(self):
        mock_result = {"items": [], "items_total": 0}
        with patch(
            "imio.smartweb.core.contents.rest.search.endpoint.api.portal.get_current_language",
            return_value="nl",
        ):
            with patch.object(SearchHandler, "search", return_value=mock_result):
                handler = ExtendedSearchHandler(self.portal, self.request)
                result = handler.search(
                    {"_core": "news", "SearchableText": "test query"}
                )
                self.assertIsNotNone(result)

    def test_search_with_unknown_core_skips_adapt(self):
        mock_result = {"items": [], "items_total": 0}
        with patch.object(SearchHandler, "search", return_value=mock_result):
            handler = ExtendedSearchHandler(self.portal, self.request)
            # Unknown core means _core_query returns None → no query update → no "core" key
            result = handler.search({"_core": "unknown"})
            self.assertEqual(result, mock_result)


class TestSearchGet(ImioSmartwebTestCase):
    """Tests for SearchGet REST service"""

    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_search_get_reply(self):
        mock_result = {"items": [], "items_total": 0}
        with patch.object(ExtendedSearchHandler, "search", return_value=mock_result):
            service = SearchGet()
            service.context = self.portal
            service.request = self.request
            self.request.form = {"SearchableText": "test"}
            result = service.reply()
            self.assertEqual(result, mock_result)


class TestSearchBrowserView(ImioSmartwebTestCase):
    """Tests for Search browser view in browser/search/search.py"""

    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def _get_search_view(self):
        return queryMultiAdapter((self.portal, self.request), name="search")

    def test_results_news(self):
        self.request.form["SearchableText"] = "kamoulox"
        search = self._get_search_view()
        results = search.results_news()
        self.assertIsNotNone(results)

    def test_get_item_url_unknown_type_raises(self):
        search = self._get_search_view()
        item = MagicMock()
        item.portal_type = "unknown.portal.type"
        with self.assertRaises(NotImplementedError):
            search.get_item_url(item)

    def test_get_item_url_no_view_raises(self):
        search = self._get_search_view()
        item = MagicMock()
        item.portal_type = "imio.news.NewsItem"
        # No NewsView in catalog → should raise ValueError
        with self.assertRaises(ValueError):
            search.get_item_url(item)

    def test_get_item_url_with_news_view(self):
        search = self._get_search_view()
        news_view = api.content.create(
            container=self.portal,
            type="imio.smartweb.NewsView",
            id="test-news-view-search",
        )
        api.content.transition(news_view, "publish")
        item = MagicMock()
        item.portal_type = "imio.news.NewsItem"
        item.Title = "My News Item"
        item.UID = "abc123"
        url = search.get_item_url(item)
        self.assertIn(news_view.absolute_url(), url)
        self.assertIn("abc123", url)
