# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.rest.events.view import EventsViewView  # noqa: F401
from imio.smartweb.core.contents.rest.news.view import NewsViewView  # noqa: F401
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from unittest.mock import patch
from zope.component import queryMultiAdapter

import requests_mock


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
