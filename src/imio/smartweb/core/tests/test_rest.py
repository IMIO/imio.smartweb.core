# -*- coding: utf-8 -*-

from freezegun import freeze_time
from imio.smartweb.core import config
from imio.smartweb.core.contents.rest.directory.endpoint import DirectoryEndpoint
from imio.smartweb.core.contents.rest.events.endpoint import EventsEndpoint
from imio.smartweb.core.contents.rest.events.endpoint import expand_occurences
from imio.smartweb.core.contents.rest.news.endpoint import NewsEndpoint
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_ACCEPTANCE_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import get_json
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession
from unittest.mock import patch
from urllib.parse import urlparse
from urllib.parse import parse_qs
from zope.component import queryMultiAdapter
from zope.publisher.browser import TestRequest

import json
import requests_mock
import transaction


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
        m.get(url, text=json.dumps([]))
        call = endpoint()
        self.assertEqual(call, [])

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
            "http://localhost:8080/Plone/@search?"
            "selected_agendas={}&"
            "portal_type=imio.events.Event&"
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
        m.get(url, text=json.dumps([]))
        call = endpoint()
        self.assertEqual(call, [])

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

    @freeze_time("2022-11-10")
    def test_expand_occurences(self):
        # test without occurence
        events = [
            {
                "start": "2022-11-13T12:00:00+00:00",
                "end": "2022-11-13T13:00:00+00:00",
                "recurrence": None,
                "open_end": False,
                "whole_day": False,
            }
        ]
        expanded_events = expand_occurences(events)
        self.assertEqual(len(expanded_events), 1)
        events = [
            {
                "start": "2022-11-13T12:00:00+00:00",
                "end": "2022-11-14T13:00:00+00:00",
                "recurrence": None,
                "open_end": False,
                "whole_day": False,
            }
        ]
        expanded_events = expand_occurences(events)
        self.assertEqual(len(expanded_events), 1)

        # test range start for occurences
        events = [
            {
                "start": "2022-11-01T12:00:00+00:00",
                "end": "2022-11-01T13:00:00+00:00",
                "recurrence": "RRULE:FREQ=WEEKLY;COUNT=5",
                "open_end": False,
                "whole_day": False,
            }
        ]
        expanded_events = expand_occurences(events)
        self.assertEqual(len(expanded_events), 3)

        # test occurences data
        events = [
            {
                "start": "2022-11-13T12:00:00+00:00",
                "end": "2022-11-13T13:00:00+00:00",
                "recurrence": "RRULE:FREQ=WEEKLY;COUNT=5",
                "open_end": False,
                "whole_day": False,
            }
        ]
        expanded_events = expand_occurences(events)
        self.assertEqual(len(expanded_events), 5)
        self.assertEqual(expanded_events[-1]["start"], "2022-12-11T12:00:00+00:00")
        self.assertEqual(expanded_events[-1]["end"], "2022-12-11T13:00:00+00:00")
        events = [
            {
                "start": "2022-11-13T12:00:00+00:00",
                "end": "2022-11-13T12:00:00+00:00",
                "recurrence": "RRULE:FREQ=WEEKLY;COUNT=5",
                "open_end": False,
                "whole_day": True,
            }
        ]
        expanded_events = expand_occurences(events)
        self.assertEqual(expanded_events[-1]["start"], "2022-12-11T12:00:00+00:00")
        self.assertEqual(expanded_events[-1]["end"], "2022-12-12T11:59:59+00:00")
        events = [
            {
                "start": "2022-11-13T00:00:00+00:00",
                "end": "2022-11-13T23:59:59+00:00",
                "recurrence": "RRULE:FREQ=WEEKLY;COUNT=5",
                "open_end": True,
                "whole_day": True,
            }
        ]
        expanded_events = expand_occurences(events)
        self.assertEqual(expanded_events[-1]["start"], "2022-12-11T00:00:00+00:00")
        self.assertEqual(expanded_events[-1]["end"], "2022-12-11T23:59:59+00:00")

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
        m.get(url, text=json.dumps([]))
        call = endpoint()
        self.assertEqual(call, [])

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
