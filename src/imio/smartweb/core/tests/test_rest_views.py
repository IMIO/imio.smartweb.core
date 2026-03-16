# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.rest.base import BaseEndpoint
from imio.smartweb.core.contents.rest.directory.view import (
    DirectoryViewView,
)  # noqa: F401
from imio.smartweb.core.contents.rest.events.view import EventsViewView  # noqa: F401
from imio.smartweb.core.contents.rest.news.endpoint import NewsEndpoint
from imio.smartweb.core.contents.rest.news.endpoint import NewsEndpointGet
from imio.smartweb.core.contents.rest.news.endpoint import NewsFiltersEndpoint
from imio.smartweb.core.contents.rest.news.endpoint import NewsFiltersEndpointGet
from imio.smartweb.core.contents.rest.news.view import NewsViewView  # noqa: F401
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from unittest.mock import patch
from zope.component import queryMultiAdapter

import requests_mock


_NEWS_ENDPOINT_MODULE = "imio.smartweb.core.contents.rest.news.endpoint"
_BASE_MODULE = "imio.smartweb.core.contents.rest.base"
_DIR_VIEW_MODULE = "imio.smartweb.core.contents.rest.directory.view"


class TestBaseRestView(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    def setUp(self):
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.events_view = api.content.create(
            container=self.portal,
            type="imio.smartweb.EventsView",
            title="Events view",
            id="events-view",
        )

    def _get_view(self):
        return queryMultiAdapter((self.events_view, self.request), name="view")

    def test_batch_size(self):
        self.events_view.nb_results = 12
        view = self._get_view()
        self.assertEqual(view.batch_size, 12)

    def test_local_query_url(self):
        view = self._get_view()
        self.assertIn("@results", view.local_query_url)
        self.assertIn(self.events_view.absolute_url(), view.local_query_url)

    def test_local_filters_query_url(self):
        view = self._get_view()
        self.assertIn("@results-filters", view.local_filters_query_url)

    def test_orientation(self):
        self.events_view.orientation = "portrait"
        view = self._get_view()
        self.assertEqual(view.orientation, "portrait")

    def test_current_language(self):
        view = self._get_view()
        self.assertIn(view.current_language, ["en", "fr", "nl", "de"])

    def test_context_authenticated_user(self):
        view = self._get_view()
        # In tests we have a logged-in user
        self.assertFalse(view.context_authenticated_user)

    def test_view_path(self):
        view = self._get_view()
        path = view.view_path
        self.assertIn("/plone/", path)
        self.assertNotIn("http://", path)
        self.assertNotIn("https://", path)

    def test_format_address_full(self):
        view = self._get_view()
        result = view._format_address(
            street="Rue de la Loi",
            number="16",
            zipcode=1000,
            city="Bruxelles",
            country="Belgique",
        )
        self.assertIn("Rue de la Loi", result)
        self.assertIn("16", result)
        self.assertIn("1000", result)
        self.assertIn("Bruxelles", result)
        self.assertIn("Belgique", result)

    def test_format_address_partial(self):
        view = self._get_view()
        # Only city and zipcode
        result = view._format_address(zipcode=4000, city="Liège")
        self.assertIn("4000", result)
        self.assertIn("Liège", result)
        self.assertNotIn("/", result)

    def test_format_address_empty(self):
        view = self._get_view()
        result = view._format_address()
        self.assertEqual(result, "")

    def test_direct_access_without_uuid(self):
        self.request.environ["QUERY_STRING"] = ""
        view = self._get_view()
        self.assertFalse(view.direct_access)

    @requests_mock.Mocker()
    def test_direct_access_with_uuid_no_referer(self, m):
        uuid = "abc123def456"
        self.request.environ["QUERY_STRING"] = f"u={uuid}"
        self.request.environ["HTTP_REFERER"] = ""
        mock_data = {"items": [{"UID": uuid, "title": "Test Event"}], "items_total": 1}
        m.get(requests_mock.ANY, json=mock_data)
        view = self._get_view()
        self.assertTrue(view.direct_access)
        self.assertIsNotNone(view.item)
        self.assertEqual(view.item.get("title"), "Test Event")

    def test_direct_access_with_referer(self):
        uuid = "abc123def456"
        self.request.environ["QUERY_STRING"] = f"u={uuid}"
        self.request.environ["HTTP_REFERER"] = "http://some-referer.be"
        view = self._get_view()
        self.assertFalse(view.direct_access)


class TestSeoHiddenReactLinks(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    def setUp(self):
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.events_view = api.content.create(
            container=self.portal,
            type="imio.smartweb.EventsView",
            title="Events view",
            id="events-view",
        )
        self.news_view = api.content.create(
            container=self.portal,
            type="imio.smartweb.NewsView",
            title="News view",
            id="news-view",
        )
        self.directory_view = api.content.create(
            container=self.portal,
            type="imio.smartweb.DirectoryView",
            title="Directory view",
            id="directory-view",
        )

    def _mock_endpoint_data(self, items=None):
        return {"items": items or [], "items_total": len(items or [])}

    @patch("imio.smartweb.core.contents.rest.view.get_endpoint_data")
    @patch("imio.smartweb.core.contents.rest.view.format_sitemap_items")
    def test_seo_hidden_react_links_events(self, mock_format, mock_endpoint):
        mock_endpoint.return_value = {"items": [], "items_total": 0}
        mock_format.return_value = []
        view = queryMultiAdapter((self.events_view, self.request), name="seo_html")
        view()
        self.assertEqual(view.total, 0)
        self.assertEqual(view.get_data, [])
        self.assertEqual(view.default_view, self.events_view.absolute_url())

    @patch("imio.smartweb.core.contents.rest.view.get_endpoint_data")
    @patch("imio.smartweb.core.contents.rest.view.format_sitemap_items")
    def test_seo_hidden_react_links_label_events(self, mock_format, mock_endpoint):
        mock_endpoint.return_value = {"items": [], "items_total": 0}
        mock_format.return_value = []
        view = queryMultiAdapter((self.events_view, self.request), name="seo_html")
        view()
        label = view.label
        self.assertIsNotNone(label)

    @patch("imio.smartweb.core.contents.rest.view.get_endpoint_data")
    @patch("imio.smartweb.core.contents.rest.view.format_sitemap_items")
    def test_seo_hidden_react_links_label_news(self, mock_format, mock_endpoint):
        mock_endpoint.return_value = {"items": [], "items_total": 0}
        mock_format.return_value = []
        view = queryMultiAdapter((self.news_view, self.request), name="seo_html")
        view()
        label = view.label
        self.assertIsNotNone(label)

    @patch("imio.smartweb.core.contents.rest.view.get_endpoint_data")
    @patch("imio.smartweb.core.contents.rest.view.format_sitemap_items")
    def test_seo_hidden_react_links_label_directory(self, mock_format, mock_endpoint):
        mock_endpoint.return_value = {"items": [], "items_total": 0}
        mock_format.return_value = []
        view = queryMultiAdapter((self.directory_view, self.request), name="seo_html")
        view()
        label = view.label
        self.assertIsNotNone(label)

    @patch("imio.smartweb.core.contents.rest.view.get_endpoint_data")
    @patch("imio.smartweb.core.contents.rest.view.format_sitemap_items")
    def test_seo_hidden_react_links_items_total(self, mock_format, mock_endpoint):
        # items_total from endpoint data is used as total (items list stays empty for template compat)
        mock_endpoint.return_value = {"items": [], "items_total": 42}
        mock_format.return_value = []
        view = queryMultiAdapter((self.news_view, self.request), name="seo_html")
        view()
        self.assertEqual(view.total, 42)
        self.assertEqual(len(view.get_data), 0)

    @patch("imio.smartweb.core.contents.rest.view.get_endpoint_data")
    @patch("imio.smartweb.core.contents.rest.view.format_sitemap_items")
    def test_seo_hidden_react_links_batching(self, mock_format, mock_endpoint):
        mock_endpoint.return_value = {"items": [], "items_total": 50}
        mock_format.return_value = []
        self.request.form["b_start"] = "10"
        self.request.form["b_size"] = "20"
        view = queryMultiAdapter((self.events_view, self.request), name="seo_html")
        view()
        self.assertEqual(view.b_start, 10)
        self.assertEqual(view.b_size, 20)
        self.assertEqual(view.total, 50)


class TestEventsViewView(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    def setUp(self):
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.events_view = api.content.create(
            container=self.portal,
            type="imio.smartweb.EventsView",
            title="Events view",
            id="events-view",
        )

    def _get_view(self):
        return queryMultiAdapter((self.events_view, self.request), name="view")

    def _make_event_data(self, **kwargs):
        base = {
            "title": "Test Event",
            "text": "Event text",
            "description": "A test event description",
            "street": "Rue de la Loi",
            "number": "16",
            "city": "Bruxelles",
            "zipcode": 1000,
            "country": None,
            "contact_phone": "+32 2 123 45 67",
            "contact_email": None,
            "event_url": "https://kamoulox.be/event",
            "event_type": None,
            "start": "2024-06-15T09:00:00",
            "end": "2024-06-15T18:00:00",
            "whole_day": False,
            "geolocation": None,
            "image": {},
        }
        base.update(kwargs)
        return base

    def test_formated_event_basic(self):
        view = self._get_view()
        data = self._make_event_data()
        result = view._formated_event(data)
        self.assertEqual(result["name"], "Test Event")
        self.assertEqual(result["text"], "Event text")
        self.assertIn("15/06/2024", result["period_text"])
        self.assertIn("09:00", result["period_text"])

    def test_formated_event_whole_day(self):
        view = self._get_view()
        data = self._make_event_data(whole_day=True)
        result = view._formated_event(data)
        self.assertIn("15/06/2024", result["period_text"])
        # Whole day: no time in period_text
        self.assertNotIn("09:00", result["period_text"])

    def test_formated_event_with_country(self):
        view = self._get_view()
        data = self._make_event_data(country={"title": "Belgique", "token": "be"})
        result = view._formated_event(data)
        self.assertIn("Belgique", result["address"])

    def test_formated_event_without_address(self):
        view = self._get_view()
        data = self._make_event_data(street=None, number=None, city=None, zipcode=None)
        result = view._formated_event(data)
        self.assertIsNone(result["address"])

    def test_formated_event_with_email(self):
        view = self._get_view()
        data = self._make_event_data(contact_email="info@kamoulox.be")
        result = view._formated_event(data)
        self.assertIn("info@kamoulox.be", result["email"])

    def test_formated_event_with_event_type(self):
        view = self._get_view()
        data = self._make_event_data(
            event_type={"title": "Concert", "token": "concert"}
        )
        result = view._formated_event(data)
        self.assertIn("Concert", result["event_type"])

    def test_formated_event_with_geolocation(self):
        view = self._get_view()
        data = self._make_event_data(geolocation={"latitude": 50.85, "longitude": 4.35})
        result = view._formated_event(data)
        self.assertEqual(result["geolocation"], (50.85, 4.35))

    def test_formated_event_no_geolocation(self):
        view = self._get_view()
        data = self._make_event_data(geolocation={"latitude": None, "longitude": None})
        result = view._formated_event(data)
        self.assertIsNone(result["geolocation"])

    def test_formated_event_with_portrait_affiche_image(self):
        view = self._get_view()
        image_url = "https://kamoulox.be/@@images/image-portrait.jpeg"
        data = self._make_event_data(
            image={
                "scales": {
                    "portrait_affiche": {
                        "download": image_url,
                        "width": 440,
                        "height": 782,
                    }
                }
            }
        )
        result = view._formated_event(data)
        self.assertEqual(result["image_url"], image_url)

    def test_formated_event_with_fallback_download_image(self):
        view = self._get_view()
        image_url = "https://kamoulox.be/@@images/image.jpeg"
        data = self._make_event_data(image={"download": image_url})
        result = view._formated_event(data)
        self.assertEqual(result["image_url"], image_url)

    def test_formated_event_without_image(self):
        view = self._get_view()
        data = self._make_event_data(image={})
        result = view._formated_event(data)
        self.assertIsNone(result["image_url"])

    def test_events_view_properties(self):
        self.events_view.display_map = True
        self.events_view.only_past_events = False
        self.events_view.display_agendas_titles = True
        self.events_view.show_categories_or_topics = "category"
        view = self._get_view()
        self.assertTrue(view.display_map)
        self.assertFalse(view.only_past_events)
        self.assertTrue(view.display_agendas_titles)
        self.assertEqual(view.show_categories_or_topics, "category")
        # propose_url is from registry - just check it doesn't raise
        self.assertIsNone(view.propose_url)


class TestNewsViewView(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    def setUp(self):
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.news_view = api.content.create(
            container=self.portal,
            type="imio.smartweb.NewsView",
            title="News view",
            id="news-view",
        )

    def _get_view(self):
        return queryMultiAdapter((self.news_view, self.request), name="view")

    def _make_news_data(self, **kwargs):
        base = {
            "title": "Test News",
            "text": "News text",
            "description": "A news description",
            "contact_phone": "+32 2 123 45 67",
            "contact_email": None,
            "site_url": "https://kamoulox.be/news",
            "image": {},
        }
        base.update(kwargs)
        return base

    def test_formated_news_basic(self):
        view = self._get_view()
        data = self._make_news_data()
        result = view._formated_news(data)
        self.assertEqual(result["name"], "Test News")
        self.assertEqual(result["text"], "News text")
        self.assertEqual(result["url"], "https://kamoulox.be/news")

    def test_formated_news_with_email(self):
        view = self._get_view()
        data = self._make_news_data(contact_email="news@kamoulox.be")
        result = view._formated_news(data)
        self.assertIn("news@kamoulox.be", result["email"])

    def test_formated_news_with_portrait_affiche_image(self):
        view = self._get_view()
        image_url = "https://kamoulox.be/@@images/image-portrait.jpeg"
        data = self._make_news_data(
            image={
                "scales": {
                    "portrait_affiche": {
                        "download": image_url,
                        "width": 440,
                        "height": 782,
                    }
                }
            }
        )
        result = view._formated_news(data)
        self.assertEqual(result["image_url"], image_url)

    def test_formated_news_with_fallback_download_image(self):
        view = self._get_view()
        image_url = "https://kamoulox.be/@@images/image.jpeg"
        data = self._make_news_data(image={"download": image_url})
        result = view._formated_news(data)
        self.assertEqual(result["image_url"], image_url)

    def test_formated_news_without_image(self):
        view = self._get_view()
        data = self._make_news_data(image={})
        result = view._formated_news(data)
        self.assertIsNone(result["image_url"])

    def test_news_view_properties(self):
        self.news_view.display_newsfolders_titles = True
        self.news_view.show_categories_or_topics = "topic"
        view = self._get_view()
        self.assertTrue(view.display_newsfolders_titles)
        self.assertEqual(view.show_categories_or_topics, "topic")
        # propose_url from registry - just check it doesn't raise
        self.assertIsNone(view.propose_url)


class TestBaseNewsEndpoint(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.news_view = api.content.create(
            container=self.portal,
            type="imio.smartweb.NewsView",
            title="News view",
        )

    def _make_endpoint(self):
        return NewsEndpoint(self.news_view, self.request)

    def _make_item(self, with_image=False, sub_items=None):
        item = {
            "@id": "http://localhost:8080/Plone/news/item1",
            "@type": "imio.news.NewsItem",
            "modified": "2025-01-01T00:00:00+00:00",
        }
        if with_image:
            item["image"] = {"scales": {}}
        if sub_items is not None:
            item["items"] = sub_items
        return item

    # --- __call__ ---

    def test_call_returns_empty_dict_when_super_returns_none(self):
        endpoint = self._make_endpoint()
        with patch.object(BaseEndpoint, "__call__", return_value=None):
            result = endpoint()
        self.assertEqual(result, {})

    def test_call_returns_results_unchanged_when_no_items(self):
        endpoint = self._make_endpoint()
        with patch.object(BaseEndpoint, "__call__", return_value={"items_total": 0}):
            result = endpoint()
        self.assertEqual(result, {"items_total": 0})

    def test_call_processes_image_when_result_has_image(self):
        endpoint = self._make_endpoint()
        item = self._make_item(with_image=True)
        with patch.object(BaseEndpoint, "__call__", return_value={"items": [item]}):
            with patch.object(endpoint, "convert_cached_image_scales") as mock_convert:
                endpoint()
        self.assertTrue(mock_convert.called)
        first_call_args = mock_convert.call_args_list[0][0]
        self.assertIs(first_call_args[0], item)

    def test_call_skips_image_processing_when_no_image(self):
        endpoint = self._make_endpoint()
        item = self._make_item(with_image=False)
        with patch.object(BaseEndpoint, "__call__", return_value={"items": [item]}):
            with patch.object(endpoint, "convert_cached_image_scales") as mock_convert:
                endpoint()
        mock_convert.assert_not_called()

    def test_call_processes_sub_items_of_type_image(self):
        endpoint = self._make_endpoint()
        sub_item = {
            "@id": "http://localhost:8080/Plone/news/item1/image1",
            "@type": "Image",
        }
        item = self._make_item(sub_items=[sub_item])
        with patch.object(BaseEndpoint, "__call__", return_value={"items": [item]}):
            with patch.object(endpoint, "convert_cached_image_scales") as mock_convert:
                endpoint()
        self.assertTrue(mock_convert.called)
        call_args = mock_convert.call_args_list[0][0]
        self.assertIs(call_args[0], sub_item)

    def test_call_skips_sub_items_not_of_type_image(self):
        endpoint = self._make_endpoint()
        sub_item = {
            "@id": "http://localhost:8080/Plone/news/item1/file1",
            "@type": "File",
        }
        item = self._make_item(sub_items=[sub_item])
        with patch.object(BaseEndpoint, "__call__", return_value={"items": [item]}):
            with patch.object(endpoint, "convert_cached_image_scales") as mock_convert:
                endpoint()
        mock_convert.assert_not_called()

    def test_call_uses_context_orientation_for_main_image(self):
        self.news_view.orientation = "portrait"
        endpoint = self._make_endpoint()
        item = self._make_item(with_image=True)
        with patch.object(BaseEndpoint, "__call__", return_value={"items": [item]}):
            with patch.object(endpoint, "convert_cached_image_scales") as mock_convert:
                endpoint()
        call_kwargs = mock_convert.call_args_list[0][1]
        self.assertEqual(call_kwargs.get("orientation"), "portrait")

    def test_call_returns_items_in_result(self):
        endpoint = self._make_endpoint()
        items = [self._make_item()]
        with patch.object(BaseEndpoint, "__call__", return_value={"items": items}):
            with patch.object(endpoint, "convert_cached_image_scales"):
                result = endpoint()
        self.assertIn("items", result)
        self.assertEqual(len(result["items"]), 1)


class TestGetNewsFoldersUidsAndTitle(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.news_view = api.content.create(
            container=self.portal,
            type="imio.smartweb.NewsView",
            title="News view",
        )

    def _make_endpoint(self):
        return NewsEndpoint(self.news_view, self.request)

    def _entity_data(self):
        return {
            "items": [
                {
                    "@id": "http://localhost:8080/Plone/manage-news",
                    "@type": "imio.news.Entity",
                    "UID": "entity-uid-123",
                    "title": "Test Entity",
                }
            ]
        }

    def _newsfolders_data(self):
        return {
            "items": [
                {"UID": "folder-uid-1", "title": "News folder : Administration"},
                {"UID": "folder-uid-2", "title": "News Folder : CPAS"},
            ]
        }

    def test_returns_uids_list(self):
        endpoint = self._make_endpoint()
        with patch(f"{_NEWS_ENDPOINT_MODULE}.get_json") as mock_get:
            mock_get.side_effect = [self._entity_data(), self._newsfolders_data()]
            uids, _ = endpoint._get_news_folders_uids_and_title_from_entity("some-uid")
        self.assertEqual(uids, ["folder-uid-1", "folder-uid-2"])

    def test_returns_title_dict(self):
        endpoint = self._make_endpoint()
        with patch(f"{_NEWS_ENDPOINT_MODULE}.get_json") as mock_get:
            mock_get.side_effect = [self._entity_data(), self._newsfolders_data()]
            _, data = endpoint._get_news_folders_uids_and_title_from_entity("some-uid")
        self.assertEqual(data["folder-uid-1"], "News folder : Administration")
        self.assertEqual(data["folder-uid-2"], "News Folder : CPAS")

    def test_makes_two_get_json_calls(self):
        endpoint = self._make_endpoint()
        with patch(f"{_NEWS_ENDPOINT_MODULE}.get_json") as mock_get:
            mock_get.side_effect = [self._entity_data(), self._newsfolders_data()]
            endpoint._get_news_folders_uids_and_title_from_entity("some-uid")
        self.assertEqual(mock_get.call_count, 2)

    def test_first_call_uses_entity_uid_in_url(self):
        endpoint = self._make_endpoint()
        with patch(f"{_NEWS_ENDPOINT_MODULE}.get_json") as mock_get:
            mock_get.side_effect = [self._entity_data(), self._newsfolders_data()]
            endpoint._get_news_folders_uids_and_title_from_entity("my-entity-uid")
        first_url = mock_get.call_args_list[0][0][0]
        self.assertIn("my-entity-uid", first_url)


class TestNewsEndpointQueryUrl(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.news_view = api.content.create(
            container=self.portal,
            type="imio.smartweb.NewsView",
            title="News view",
        )
        self.news_view.nb_results = 10
        self.uids = ["folder-uid-admin", "folder-uid-cpas"]
        self.data = {
            "folder-uid-admin": "News folder : Administration",
            "folder-uid-cpas": "News Folder : CPAS",
        }

    def tearDown(self):
        self.request.form.pop("batch_size", None)

    def _get_query_url(self, selected=None, batch_size=0):
        if selected is not None:
            self.news_view.selected_news_folder = selected
        endpoint = NewsEndpoint(self.news_view, self.request, batch_size=batch_size)
        with patch(f"{_NEWS_ENDPOINT_MODULE}.api") as mock_api:
            mock_api.portal.get_registry_record.return_value = "entity-uid-123"
            with patch(f"{_BASE_MODULE}.api") as mock_base_api:
                mock_base_api.portal.get_current_language.return_value = "fr"
                with patch.object(
                    endpoint,
                    "_get_news_folders_uids_and_title_from_entity",
                    return_value=(self.uids, self.data),
                ):
                    return endpoint.query_url

    def test_uses_selected_folder_when_in_uids(self):
        url = self._get_query_url(selected="folder-uid-cpas")
        self.assertIn("folder-uid-cpas", url)

    def test_falls_back_to_administration_folder_when_selected_not_in_uids(self):
        url = self._get_query_url(selected="unknown-uid")
        self.assertIn("folder-uid-admin", url)

    def test_falls_back_to_first_uid_when_no_administration_folder(self):
        self.uids = ["folder-uid-1", "folder-uid-2"]
        self.data = {
            "folder-uid-1": "News Folder : CPAS",
            "folder-uid-2": "News Folder : OCMW",
        }
        url = self._get_query_url(selected="unknown-uid")
        self.assertIn("folder-uid-1", url)

    def test_batch_size_from_request_form(self):
        self.request.form["batch_size"] = "5"
        url = self._get_query_url(selected=self.uids[0])
        self.assertIn("b_size=5", url)

    def test_batch_size_uses_context_nb_results_when_endpoint_batch_size_zero(self):
        self.news_view.nb_results = 15
        url = self._get_query_url(selected=self.uids[0], batch_size=0)
        self.assertIn("b_size=15", url)

    def test_batch_size_from_endpoint_when_non_zero(self):
        url = self._get_query_url(selected=self.uids[0], batch_size=7)
        self.assertIn("b_size=7", url)

    def test_query_url_contains_remote_endpoint(self):
        url = self._get_query_url(selected=self.uids[0])
        self.assertIn("@search_newsitems", url)

    def test_news_filters_query_url_contains_filters_endpoint(self):
        endpoint = NewsFiltersEndpoint(self.news_view, self.request)
        self.news_view.selected_news_folder = self.uids[0]
        with patch(f"{_NEWS_ENDPOINT_MODULE}.api") as mock_api:
            mock_api.portal.get_registry_record.return_value = "entity-uid-123"
            with patch(f"{_BASE_MODULE}.api") as mock_base_api:
                mock_base_api.portal.get_current_language.return_value = "fr"
                with patch.object(
                    endpoint,
                    "_get_news_folders_uids_and_title_from_entity",
                    return_value=(self.uids, self.data),
                ):
                    url = endpoint.query_url
        self.assertIn("@search-filters", url)

    def test_query_url_contains_entity_uid(self):
        url = self._get_query_url(selected=self.uids[0])
        self.assertIn("entity-uid-123", url)


class TestNewsEndpointGetService(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.news_view = api.content.create(
            container=self.portal,
            type="imio.smartweb.NewsView",
            title="News view",
        )

    def _make_service(self, cls):
        service = object.__new__(cls)
        service.context = self.news_view
        service.request = self.request
        return service

    def test_reply_calls_news_endpoint_and_returns_result(self):
        service = self._make_service(NewsEndpointGet)
        expected = {"items": [], "items_total": 0}
        with patch.object(NewsEndpoint, "__call__", return_value=expected):
            result = service.reply()
        self.assertEqual(result, expected)

    def test_reply_for_given_object_uses_given_context(self):
        service = self._make_service(NewsEndpointGet)
        other_view = api.content.create(
            container=self.portal,
            type="imio.smartweb.NewsView",
            title="Other News view",
        )
        captured = []

        def capture_call(self_ep):
            captured.append(self_ep.context)
            return {}

        with patch.object(NewsEndpoint, "__call__", capture_call):
            service.reply_for_given_object(other_view, self.request)
        self.assertIs(captured[0], other_view)

    def test_reply_for_given_object_passes_batch_size(self):
        service = self._make_service(NewsEndpointGet)
        captured = []

        def capture_call(self_ep):
            captured.append(self_ep.batch_size)
            return {}

        with patch.object(NewsEndpoint, "__call__", capture_call):
            service.reply_for_given_object(self.news_view, self.request, batch_size=8)
        self.assertEqual(captured[0], 8)

    def test_reply_for_given_object_passes_fullobjects(self):
        service = self._make_service(NewsEndpointGet)
        captured = []

        def capture_call(self_ep):
            captured.append(self_ep.fullobjects)
            return {}

        with patch.object(NewsEndpoint, "__call__", capture_call):
            service.reply_for_given_object(self.news_view, self.request, fullobjects=0)
        self.assertEqual(captured[0], 0)

    def test_news_filters_reply_calls_filters_endpoint(self):
        service = self._make_service(NewsFiltersEndpointGet)
        expected = {"filters": []}
        with patch.object(NewsFiltersEndpoint, "__call__", return_value=expected):
            result = service.reply()
        self.assertEqual(result, expected)


class TestDirectoryViewView(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    def setUp(self):
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.directory_view = api.content.create(
            container=self.portal,
            type="imio.smartweb.DirectoryView",
            title="Directory view",
            id="directory-view",
        )

    def _get_view(self):
        return queryMultiAdapter((self.directory_view, self.request), name="view")

    def _make_contact_data(self, **kwargs):
        # NOTE: "type" key is intentionally omitted from the base dict.
        # data.get("type", {}).get("title") raises AttributeError if type=None.
        base = {
            "title": "Test Contact",
            "subtitle": None,
            "number": "1",
            "street": "Rue de la Paix",
            "city": "Namur",
            "zipcode": 5000,
            "country": None,
            "phones": [],
            "mails": [],
            "urls": [],
            "description": None,
            "taxonomy_contact_category": [],
            "geolocation": {},
            "image": {},
        }
        base.update(kwargs)
        return base

    # --- _formated_contact: name ---

    def test_formated_contact_basic_name(self):
        view = self._get_view()
        data = self._make_contact_data()
        result = view._formated_contact(data)
        self.assertEqual(result["name"], "Test Contact")

    def test_formated_contact_language_specific_title_takes_priority(self):
        view = self._get_view()
        data = self._make_contact_data(title="Fallback", title_fr="French Title")
        with patch(f"{_DIR_VIEW_MODULE}.api") as mock_api:
            mock_api.portal.get_current_language.return_value = "fr"
            result = view._formated_contact(data)
        self.assertEqual(result["name"], "French Title")

    def test_formated_contact_falls_back_to_title_when_lang_specific_missing(self):
        view = self._get_view()
        data = self._make_contact_data(title="Fallback Title")
        with patch(f"{_DIR_VIEW_MODULE}.api") as mock_api:
            mock_api.portal.get_current_language.return_value = "nl"
            result = view._formated_contact(data)
        self.assertEqual(result["name"], "Fallback Title")

    # --- _formated_contact: subtitle ---

    def test_formated_contact_subtitle(self):
        view = self._get_view()
        data = self._make_contact_data(subtitle="A subtitle")
        result = view._formated_contact(data)
        self.assertEqual(result["subtitle"], "A subtitle")

    # --- _formated_contact: phones ---

    def test_formated_contact_with_phone(self):
        view = self._get_view()
        data = self._make_contact_data(phones=[{"number": "+32 81 12 34 56"}])
        result = view._formated_contact(data)
        self.assertEqual(result["phone"], "+32 81 12 34 56")

    def test_formated_contact_without_phone(self):
        view = self._get_view()
        data = self._make_contact_data(phones=[])
        result = view._formated_contact(data)
        self.assertIsNone(result["phone"])

    # --- _formated_contact: mails ---

    def test_formated_contact_with_email(self):
        view = self._get_view()
        data = self._make_contact_data(mails=[{"mail_address": "info@namur.be"}])
        result = view._formated_contact(data)
        self.assertIn("info@namur.be", result["email"])

    def test_formated_contact_without_email(self):
        view = self._get_view()
        data = self._make_contact_data(mails=[])
        result = view._formated_contact(data)
        self.assertIsNone(result["email"])

    # --- _formated_contact: urls ---

    def test_formated_contact_with_url(self):
        view = self._get_view()
        data = self._make_contact_data(urls=[{"url": "https://namur.be"}])
        result = view._formated_contact(data)
        self.assertEqual(result["url"], "https://namur.be")

    def test_formated_contact_without_url(self):
        view = self._get_view()
        data = self._make_contact_data(urls=[])
        result = view._formated_contact(data)
        self.assertIsNone(result["url"])

    # --- _formated_contact: description ---

    def test_formated_contact_with_description(self):
        view = self._get_view()
        data = self._make_contact_data(description="A nice description")
        result = view._formated_contact(data)
        self.assertIn("A nice description", result["description"])

    def test_formated_contact_without_description(self):
        view = self._get_view()
        data = self._make_contact_data(description=None)
        result = view._formated_contact(data)
        self.assertIsNone(result["description"])

    # --- _formated_contact: category ---

    def test_formated_contact_with_category(self):
        view = self._get_view()
        data = self._make_contact_data(
            taxonomy_contact_category=[{"title": "Library", "token": "library"}]
        )
        result = view._formated_contact(data)
        self.assertIn("Library", result["category"])

    def test_formated_contact_without_category(self):
        view = self._get_view()
        data = self._make_contact_data(taxonomy_contact_category=[])
        result = view._formated_contact(data)
        self.assertIsNone(result["category"])

    # --- _formated_contact: contact_type ---

    def test_formated_contact_with_contact_type(self):
        view = self._get_view()
        data = self._make_contact_data(type={"title": "School", "token": "school"})
        result = view._formated_contact(data)
        self.assertIn("School", result["contact_type"])

    def test_formated_contact_without_contact_type(self):
        view = self._get_view()
        # "type" key intentionally absent from base dict — defaults to {}
        data = self._make_contact_data()
        result = view._formated_contact(data)
        self.assertIsNone(result["contact_type"])

    # --- _formated_contact: geolocation ---

    def test_formated_contact_with_geolocation(self):
        view = self._get_view()
        data = self._make_contact_data(
            geolocation={"latitude": 50.46, "longitude": 4.86}
        )
        result = view._formated_contact(data)
        self.assertEqual(result["geolocation"], (50.46, 4.86))

    def test_formated_contact_without_geolocation(self):
        view = self._get_view()
        data = self._make_contact_data(geolocation=None)
        result = view._formated_contact(data)
        self.assertIsNone(result["geolocation"])

    # --- _formated_contact: image ---

    def test_formated_contact_with_portrait_affiche_image(self):
        view = self._get_view()
        image_url = "https://directory.be/@@images/image-portrait.jpeg"
        data = self._make_contact_data(
            image={
                "scales": {
                    "portrait_affiche": {
                        "download": image_url,
                        "width": 440,
                        "height": 782,
                    }
                }
            }
        )
        result = view._formated_contact(data)
        self.assertEqual(result["image_url"], image_url)

    def test_formated_contact_with_fallback_download_image(self):
        view = self._get_view()
        image_url = "https://directory.be/@@images/image.jpeg"
        data = self._make_contact_data(image={"download": image_url})
        result = view._formated_contact(data)
        self.assertEqual(result["image_url"], image_url)

    def test_formated_contact_without_image(self):
        view = self._get_view()
        data = self._make_contact_data(image={})
        result = view._formated_contact(data)
        self.assertIsNone(result["image_url"])

    # --- _formated_contact: address ---

    def test_formated_contact_with_country_in_address(self):
        view = self._get_view()
        data = self._make_contact_data(country={"title": "Belgique", "token": "be"})
        result = view._formated_contact(data)
        self.assertIn("Belgique", result["address"])

    def test_formated_contact_without_address_fields(self):
        view = self._get_view()
        data = self._make_contact_data(
            street=None, number=None, city=None, zipcode=None
        )
        result = view._formated_contact(data)
        self.assertIsNone(result["address"])

    # --- properties ---

    def test_display_map_property(self):
        self.directory_view.display_map = True
        view = self._get_view()
        self.assertTrue(view.display_map)

    def test_propose_url_from_registry(self):
        view = self._get_view()
        # Registry record not configured in tests — returns None
        self.assertIsNone(view.propose_url)

    def test_contact_property_uses_item(self):
        view = self._get_view()
        item_data = self._make_contact_data(title="My Contact")
        view._item = {"items": [item_data]}
        result = view.contact
        self.assertEqual(result["name"], "My Contact")
