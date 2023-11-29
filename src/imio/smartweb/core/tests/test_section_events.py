# -*- coding: utf-8 -*-

from datetime import datetime
from freezegun import freeze_time
from imio.smartweb.core.contents.sections.views import SECTION_ITEMS_HASH_KEY
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import get_json
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from time import sleep
from z3c.relationfield import RelationValue
from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility
from zope.component import queryMultiAdapter
from zope.intid.interfaces import IIntIds

import json
import requests_mock


class TestSectionEvents(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    def setUp(self):
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portalpage = api.content.create(
            container=self.portal,
            type="imio.smartweb.PortalPage",
            id="Portal page",
        )
        self.json_events = get_json("resources/json_rest_events.json")
        self.json_specific_event = get_json("resources/json_rest_specific_events.json")
        self.rest_events_view = api.content.create(
            container=self.portal,
            type="imio.smartweb.EventsView",
            title="Rest events view",
        )
        self.events = api.content.create(
            container=self.portalpage,
            type="imio.smartweb.SectionEvents",
            title="My events",
        )

    @requests_mock.Mocker()
    @freeze_time("2021-11-15")
    def test_events(self, m):
        intids = getUtility(IIntIds)
        self.events.related_events = "e73e6a81afea4a579cd0da2773af8d29"
        self.events.linking_rest_view = RelationValue(
            intids.getId(self.rest_events_view)
        )
        view = queryMultiAdapter((self.portalpage, self.request), name="full_view")
        self.assertIn("My events", view())
        events_view = queryMultiAdapter(
            (self.events, self.request), name="carousel_view"
        )
        self.assertEqual(events_view.items, [])
        url = "http://localhost:8080/Plone/@events?selected_agendas=e73e6a81afea4a579cd0da2773af8d29&metadata_fields=category_title&metadata_fields=start&metadata_fields=end&metadata_fields=has_leadimage&metadata_fields=modified&metadata_fields=UID&event_dates.query=2021-11-15&event_dates.range=min&b_size=6&translated_in_en=1&sort_on=event_dates"
        m.get(url, text=json.dumps(self.json_events))
        self.assertEqual(events_view.items[0][0].get("title"), "Journée de l'ATL")
        self.assertEqual(len(events_view.items[0]), 2)
        self.events.specific_related_events = ["1178188bddde4ced95a6cf8bf04c443c"]
        url = "http://localhost:8080/Plone/@events?UID=1178188bddde4ced95a6cf8bf04c443c&metadata_fields=category_title&metadata_fields=start&metadata_fields=end&metadata_fields=has_leadimage&metadata_fields=modified&metadata_fields=UID&event_dates.query=2021-11-15&event_dates.range=min&b_size=6&translated_in_en=1"
        m.get(url, text=json.dumps(self.json_specific_event))
        self.assertEqual(len(events_view.items[0]), 1)
        self.assertEqual(events_view.items[0][0].get("title"), "Bonne cheville")

    @requests_mock.Mocker()
    def test_events_modified(self, m):
        today = datetime.now()
        today_str = today.strftime("%Y-%m-%d")
        intids = getUtility(IIntIds)
        self.events.related_events = "e73e6a81afea4a579cd0da2773af8d29"
        self.events.linking_rest_view = RelationValue(
            intids.getId(self.rest_events_view)
        )
        annotations = IAnnotations(self.events)
        self.assertIsNone(annotations.get(SECTION_ITEMS_HASH_KEY))

        events_view = queryMultiAdapter(
            (self.events, self.request), name="carousel_view"
        )
        url = f"http://localhost:8080/Plone/@events?selected_agendas=e73e6a81afea4a579cd0da2773af8d29&metadata_fields=category_title&metadata_fields=start&metadata_fields=end&metadata_fields=has_leadimage&metadata_fields=modified&metadata_fields=UID&event_dates.query={today_str}&event_dates.range=min&b_size=6&translated_in_en=1&sort_on=event_dates"
        m.get(url, text=json.dumps(self.json_events))
        self.assertEqual(len(events_view.items[0]), 2)
        hash_1 = annotations.get(SECTION_ITEMS_HASH_KEY)
        self.assertIsNotNone(hash_1)
        first_modification = self.portalpage.ModificationDate()

        sleep(1)
        url = f"http://localhost:8080/Plone/@events?selected_agendas=e73e6a81afea4a579cd0da2773af8d29&metadata_fields=category_title&metadata_fields=start&metadata_fields=end&metadata_fields=has_leadimage&metadata_fields=modified&metadata_fields=UID&event_dates.query={today_str}&event_dates.range=min&b_size=6&translated_in_en=1&sort_on=event_dates"
        m.get(url, text="{}")
        self.assertEqual(len(events_view.items), 0)
        next_modification = self.portalpage.ModificationDate()
        hash_2 = annotations.get(SECTION_ITEMS_HASH_KEY)
        self.assertNotEqual(hash_1, hash_2)
        self.assertNotEqual(first_modification, next_modification)

        sleep(1)
        self.assertEqual(len(events_view.items), 0)
        last_modification = self.portalpage.ModificationDate()
        hash_3 = annotations.get(SECTION_ITEMS_HASH_KEY)
        self.assertEqual(hash_2, hash_3)
        self.assertEqual(next_modification, last_modification)

    @requests_mock.Mocker()
    def test_orientation(self, m):
        today = datetime.now()
        today_str = today.strftime("%Y-%m-%d")
        intids = getUtility(IIntIds)
        self.events.related_events = "e73e6a81afea4a579cd0da2773af8d29"
        self.events.linking_rest_view = RelationValue(
            intids.getId(self.rest_events_view)
        )
        events_view = queryMultiAdapter(
            (self.events, self.request), name="carousel_view"
        )
        url = f"http://localhost:8080/Plone/@events?selected_agendas=e73e6a81afea4a579cd0da2773af8d29&metadata_fields=category_title&metadata_fields=start&metadata_fields=end&metadata_fields=has_leadimage&metadata_fields=modified&metadata_fields=UID&event_dates.query={today_str}&event_dates.range=min&b_size=6&translated_in_en=1&sort_on=event_dates"
        m.get(url, text=json.dumps(self.json_events))

        self.assertIn("paysage_vignette", events_view.items[0][0]["image"])
        self.events.orientation = "portrait"
        self.assertIn("portrait_vignette", events_view.items[0][0]["image"])
