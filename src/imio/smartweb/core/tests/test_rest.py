# -*- coding: utf-8 -*-

from base64 import b64encode
from freezegun import freeze_time
from imio.smartweb.core import config
from imio.smartweb.core.contents.rest.base import BaseEndpoint
from imio.smartweb.core.contents.rest.directory.endpoint import DirectoryEndpoint
from imio.smartweb.core.contents.rest.events.endpoint import EventsEndpoint
from imio.smartweb.core.contents.rest.news.endpoint import NewsEndpoint
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_ACCEPTANCE_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import FakeResponse
from imio.smartweb.core.tests.utils import get_json
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_PASSWORD
from plone.restapi.testing import RelativeSession
from unittest.mock import patch
from urllib.parse import urlparse
from urllib.parse import parse_qs
from zope.component import queryMultiAdapter
from zope.event import notify
from zope.publisher.browser import TestRequest
from ZPublisher.pubevents import PubStart

import json
import requests_mock
import transaction

# Get full string when string are too long in assertEqual errors
# __import__('sys').modules['unittest.util']._MAX_LENGTH = 999999999


class SectionsFunctionalTest(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_ACCEPTANCE_TESTING

    def setUp(self):
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.json_rest_directory = get_json("resources/json_rest_directory.json")
        self.json_rest_events = get_json("resources/json_rest_events.json")
        self.json_used_iam_voc = get_json(
            "resources/json_used_iam_vocabularies_jobseeker_tourist.json"
        )
        self.json_rest_news = get_json("resources/json_rest_news.json")
        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})

        self.rest_directory = api.content.create(
            container=self.portal,
            type="imio.smartweb.DirectoryView",
            title="directory view",
        )
        api.content.transition(self.rest_directory, "publish")

        self.rest_events = api.content.create(
            container=self.portal,
            type="imio.smartweb.EventsView",
            title="events view",
        )
        self.rest_events.selected_agenda = "64f4cbee9a394a018a951f6d94452914"
        self.rest_events.selected_event_types = ["event-driven"]
        api.content.transition(self.rest_events, "publish")

        self.rest_news = api.content.create(
            container=self.portal,
            type="imio.smartweb.NewsView",
            title="news view",
        )
        self.rest_news.selected_news_folder = "64f4cbee9a394a018a951f6d94452914"
        api.content.transition(self.rest_news, "publish")

        transaction.commit()

    def tearDown(self):
        self.api_session.close()

    def traverse(self, path="/plone", method="GET"):
        request = self.layer["request"]
        request.environ["PATH_INFO"] = path
        request.environ["PATH_TRANSLATED"] = path
        request.environ["HTTP_ACCEPT"] = "application/json"
        request.environ["REQUEST_METHOD"] = method
        request.other["ACTUAL_URL"] = ""
        request.other["URL"] = ""
        request.method = method
        request.form = {}
        auth = f"{TEST_USER_ID}:{TEST_USER_PASSWORD}"
        request._auth = "Basic %s" % b64encode(auth.encode("utf8")).decode("utf8")
        notify(PubStart(request))
        return request.traverse(path)

    @freeze_time("2021-09-14 8:00:00")
    def test_convert_cached_image_scales(self):
        endpoint = BaseEndpoint(self.portal, self.request)
        modified_hash = "78fd1bab198354b6877aed44e2ea0b4d"

        item = {"@id": "http://host.com/content", "image": {"scales": {}}}
        endpoint.convert_cached_image_scales(item, modified_hash)
        self.assertNotIn("image", item.keys())
        self.assertEqual(
            item["image_vignette_scale"],
            "http://host.com/content/@@images/image/paysage_vignette?cache_key=78fd1bab198354b6877aed44e2ea0b4d",
        )
        self.assertEqual(
            item["image_affiche_scale"],
            "http://host.com/content/@@images/image/paysage_affiche?cache_key=78fd1bab198354b6877aed44e2ea0b4d",
        )
        self.assertEqual(
            item["image_full_scale"],
            "http://host.com/content/@@images/image/?cache_key=78fd1bab198354b6877aed44e2ea0b4d",
        )

        item = {"@id": "http://host.com/content", "logo": {"scales": {}}}
        endpoint.convert_cached_image_scales(item, modified_hash, "logo", ["thumb"], "")
        self.assertNotIn("logo", item.keys())
        self.assertEqual(
            item["logo_thumb_scale"],
            "http://host.com/content/@@images/logo/thumb?cache_key=78fd1bab198354b6877aed44e2ea0b4d",
        )

        item = {
            "@id": "http://host.com/content",
            "image": {"scales": {}},
            "logo": {"scales": {}},
        }
        endpoint.convert_cached_image_scales(item, modified_hash, "logo", ["thumb"], "")
        self.assertEqual(len(item.keys()), 4)
        endpoint.convert_cached_image_scales(item, modified_hash)
        self.assertEqual(len(item.keys()), 6)

    def test_get_extra_params(self):
        request = TestRequest(
            form={"taxonomy_contact_category": '("token")', "topics": "education"}
        )
        endpoint = DirectoryEndpoint(self.portal, request)
        params = endpoint.get_extra_params([])
        self.assertEqual(
            params,
            [
                'taxonomy_contact_category=("token")',
                "topics=education",
                "translated_in_en=1",
            ],
        )

        request = TestRequest(
            form={"topics": "education", "metadata_fields": ["topics", "category"]}
        )
        endpoint = DirectoryEndpoint(self.portal, request)
        params = endpoint.get_extra_params([])
        self.assertEqual(
            params,
            [
                "topics=education",
                "metadata_fields=topics",
                "metadata_fields=category",
                "translated_in_en=1",
            ],
        )

    @requests_mock.Mocker()
    def test_call_directory(self, m):
        # We don't want to make real request on authentic sources if some Mocks are missing
        rest_directory = api.content.create(
            container=self.portal,
            type="imio.smartweb.DirectoryView",
            title="My directory view",
        )
        # react additionnal fields request.
        request = TestRequest(
            form={
                "taxonomy_contact_category_for_filtering": ("token"),
                "topics": "education",
            }
        )
        endpoint = DirectoryEndpoint(rest_directory, request)
        url = endpoint.query_url
        self.assertEqual(
            url,
            "http://localhost:8080/Plone/@search?"
            "selected_entities=396907b3b1b04a97896b12cc792c77f8&"
            "portal_type=imio.directory.Contact&"
            "metadata_fields=facilities&"
            "metadata_fields=taxonomy_contact_category&"
            "metadata_fields=topics&"
            "metadata_fields=has_leadimage&"
            "fullobjects=1&"
            "sort_on=sortable_title&"
            "b_size=20&"
            "taxonomy_contact_category_for_filtering=token&"
            "topics=education&"
            "translated_in_en=1",
        )
        m.get(url, text=json.dumps({}))
        call = endpoint()
        self.assertEqual(call, {})

        rest_directory.nb_results = 30
        url = endpoint.query_url
        self.assertNotIn("b_size=20", url)
        self.assertIn("b_size=30", url)

        json_contact_category_raw_mock = get_json(
            "resources/json_contact_category_raw_mock.json"
        )
        with patch(
            "imio.smartweb.core.vocabularies.get_wca_token", return_value="kamoulox"
        ):
            url = f"{config.DIRECTORY_URL}/@vocabularies/collective.taxonomy.contact_category"
            m.get(url, text=json.dumps(json_contact_category_raw_mock))

            rest_directory.selected_categories = ["hlsm9bijb1", "9kgcmrj4lu"]
            url = endpoint.query_url
            self.assertEqual(
                url,
                "http://localhost:8080/Plone/@search?"
                "selected_entities=396907b3b1b04a97896b12cc792c77f8&"
                "portal_type=imio.directory.Contact&"
                "metadata_fields=facilities&"
                "metadata_fields=taxonomy_contact_category&"
                "metadata_fields=topics&"
                "metadata_fields=has_leadimage&"
                "fullobjects=1&"
                "sort_on=sortable_title&"
                "b_size=30&"
                "taxonomy_contact_category.query=hlsm9bijb1&"
                "taxonomy_contact_category.query=9kgcmrj4lu&"
                "taxonomy_contact_category.operator=or&"
                "taxonomy_contact_category_for_filtering=token&"
                "topics=education&"
                "translated_in_en=1",
            )

    def test_render_rest_directory(self):
        view = queryMultiAdapter((self.rest_directory, self.request), name="view")
        self.assertIn("<smartweb-annuaire", view())

    def test_rest_directory_results(self):
        params = {}
        with patch(
            "imio.smartweb.core.contents.rest.base.get_json",
            return_value=self.json_rest_directory,
        ) as mypatch:
            response = self.api_session.get("/directory-view/@results", params=params)
            patch_url = mypatch.return_value.get("@id")
            patch_urlparsed = urlparse(patch_url)
            patch_directory = parse_qs(patch_urlparsed.query)
            response_url = response.json().get("@id")
            response_urlparsed = urlparse(response_url)
            response_directory = parse_qs(response_urlparsed.query)
            self.assertEqual(patch_directory, response_directory)

    @requests_mock.Mocker()
    @freeze_time("2021-11-15")
    def test_call_events(self, m):
        self.rest_events.selected_agenda = "64f4cbee9a394a018a951f6d94452914"
        self.rest_events.selected_event_types = ["event-driven"]
        endpoint = EventsEndpoint(self.rest_events, self.request)
        url = endpoint.query_url
        self.maxDiff = None
        self.assertEqual(
            url,
            "http://localhost:8080/Plone/@events?"
            "selected_agendas={}&"
            "metadata_fields=category&"
            "metadata_fields=topics&"
            "metadata_fields=start&"
            "metadata_fields=end&"
            "metadata_fields=has_leadimage&"
            "metadata_fields=UID&"
            "event_dates.query=2021-11-15&"
            "event_dates.range=min&"
            "sort_on=event_dates&"
            "fullobjects=1&"
            "b_size=20&"
            "event_type=event-driven&"
            "translated_in_en=1".format(self.rest_events.selected_agenda),
        )
        m.get(url, text=json.dumps({}))
        call = endpoint()
        self.assertEqual(call, {})

        self.rest_events.nb_results = 30
        url = endpoint.query_url
        self.assertNotIn("b_size=20", url)
        self.assertIn("b_size=30", url)

    def test_render_rest_events(self):
        view = queryMultiAdapter((self.rest_events, self.request), name="view")
        self.assertIn("<smartweb-events", view())

    @freeze_time("2021-11-15")
    def test_rest_events_results(self):
        params = {}
        # mock get_json from where we import/use it
        with patch(
            "imio.smartweb.core.contents.rest.base.get_json",
            return_value=self.json_rest_events,
        ) as mypatch:
            patch_url = mypatch.return_value.get("@id")
            patch_urlparsed = urlparse(patch_url)
            patch_selected_agendas = parse_qs(patch_urlparsed.query)[
                "selected_agendas"
            ][0]
            response = self.api_session.get("/events-view/@results", params=params)
            response_url = response.json().get("@id")
            response_urlparsed = urlparse(response_url)
            response_selected_agendas = parse_qs(response_urlparsed.query)[
                "selected_agendas"
            ][0]
            self.assertEqual(patch_selected_agendas, response_selected_agendas)

    @requests_mock.Mocker()
    def test_call_news(self, m):
        endpoint = NewsEndpoint(self.rest_news, self.request)
        url = endpoint.query_url
        self.maxDiff = None
        self.assertEqual(
            url,
            "http://localhost:8080/Plone/@search?"
            "selected_news_folders={}&"
            "portal_type=imio.news.NewsItem&"
            "metadata_fields=category&"
            "metadata_fields=topics&"
            "metadata_fields=has_leadimage&"
            "metadata_fields=UID&"
            "sort_on=effective&"
            "sort_order=descending&"
            "b_size=20&"
            "fullobjects=1&"
            "translated_in_en=1".format(self.rest_news.selected_news_folder),
        )
        m.get(url, text=json.dumps({}))
        call = endpoint()
        self.assertEqual(call, {})

        self.rest_news.nb_results = 30
        url = endpoint.query_url
        self.assertNotIn("b_size=20", url)
        self.assertIn("b_size=30", url)

    def test_render_rest_news(self):
        view = queryMultiAdapter((self.rest_news, self.request), name="view")
        self.assertIn("<smartweb-news", view())

    def test_rest_news_results(self):
        params = {}
        with patch(
            "imio.smartweb.core.contents.rest.base.get_json",
            return_value=self.json_rest_news,
        ) as mypatch:
            response = self.api_session.get("/news-view/@results", params=params)
            patch_url = mypatch.return_value.get("@id")
            patch_urlparsed = urlparse(patch_url)
            patch_selected_news_folders = parse_qs(patch_urlparsed.query)[
                "selected_news_folders"
            ][0]
            response_url = response.json().get("@id")
            response_urlparsed = urlparse(response_url)
            response_selected_news_folders = parse_qs(response_urlparsed.query)[
                "selected_news_folders"
            ][0]
            self.assertEqual(
                patch_selected_news_folders, response_selected_news_folders
            )

    def test_display_map(self):
        self.rest_directory = api.content.create(
            container=self.portal,
            type="imio.smartweb.DirectoryView",
            title="directory view",
        )
        self.rest_directory.display_map = True
        view = queryMultiAdapter((self.rest_directory, self.request), name="view")
        self.assertIn('display-map="True"', view())

        self.rest_events = api.content.create(
            container=self.portal,
            type="imio.smartweb.EventsView",
            title="events view",
        )
        self.rest_events.display_map = True
        view = queryMultiAdapter((self.rest_events, self.request), name="view")
        self.assertIn('display-map="True"', view())

    @patch("imio.smartweb.core.rest.authentic_sources.get_wca_token")
    @patch("imio.smartweb.core.rest.authentic_sources.requests.request")
    @patch("imio.smartweb.core.rest.authentic_sources.get_default_view_url")
    def test_request_forwarder(self, mock_view_url, mock_request, mock_get_wca_token):
        mock_view_url.return_value = "http://view-url"
        mock_get_wca_token.return_value = "kamoulox"
        mock_request.return_value = FakeResponse(
            status_code=200,
            headers={"test-header": "True"},
        )

        # traversal stack
        service = self.traverse("/plone/@news_request_forwarder/belleville/@search")
        self.assertListEqual(service.traversal_stack, ["belleville", "@search"])

        # add_smartweb_urls
        json_data = {}
        self.assertEqual(service.add_smartweb_urls(json_data), json_data)
        json_data = {"foo": "bar"}
        self.assertEqual(service.add_smartweb_urls(json_data), json_data)
        json_data = {"items": []}
        self.assertEqual(service.add_smartweb_urls(json_data), json_data)
        json_data = {"items": [{"@id": "http://news/my-news"}]}
        self.assertEqual(service.add_smartweb_urls(json_data), json_data)
        json_data = {"items": [{"@id": "http://news/my-news", "UID": "12345678"}]}
        json_result = service.add_smartweb_urls(json_data)
        self.assertIn("smartweb_url", json_result["items"][0])
        self.assertEqual(
            json_data["items"][0]["smartweb_url"], "http://view-url#/content?u=12345678"
        )

        # add_missing_metadatas
        params = {}
        self.assertEqual(
            service.add_missing_metadatas(params), {"metadata_fields": ["id", "UID"]}
        )
        params = {"fullobjects": 1}
        self.assertEqual(service.add_missing_metadatas(params), params)
        params = {"metadata_fields": ["other", "UID"]}
        self.assertEqual(
            service.add_missing_metadatas(params),
            {"metadata_fields": ["other", "UID", "id"]},
        )
        params = {"metadata_fields": ["other", "id"]}
        self.assertEqual(
            service.add_missing_metadatas(params),
            {"metadata_fields": ["other", "id", "UID"]},
        )

        # reply
        response = service.reply()
        mock_request.assert_called_with(
            "GET",
            "http://localhost:8080/Plone/belleville/@search",
            params={"metadata_fields": ["id", "UID"]},
            headers={"Accept": "application/json", "Authorization": "kamoulox"},
            json={},
        )
        self.assertEqual(response, {})
        self.assertEqual(self.request.response.status, 200)
        self.assertEqual(self.request.response.headers, {"test-header": "True"})

        service = self.traverse(
            "/plone/@events_request_forwarder/belleville/", method="POST"
        )
        service.reply()
        mock_request.assert_called_with(
            "POST",
            "http://localhost:8080/Plone/belleville",
            params={},
            headers={"Accept": "application/json", "Authorization": "kamoulox"},
            json={},
        )

        mock_request.side_effect = None
        mock_request.return_value = FakeResponse(status_code=204)
        service = self.traverse(
            "/plone/@events_request_forwarder/belleville/", method="PATCH"
        )
        response = service.reply()
        self.assertEqual(response, "")
        self.assertEqual(self.request.response.status, 204)

        self.assertEqual(
            self.api_session.get("/@directory_request_forwarder/foo/bar").text, ""
        )
        self.assertEqual(
            self.api_session.get("/@events_request_forwarder/foo/bar").text, ""
        )
        self.assertEqual(
            self.api_session.get("/@news_request_forwarder/foo/bar").text, ""
        )
