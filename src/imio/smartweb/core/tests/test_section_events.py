# -*- coding: utf-8 -*-

from freezegun import freeze_time
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import get_json
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from z3c.relationfield import RelationValue
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

    @requests_mock.Mocker()
    @freeze_time("2021-11-15")
    def test_events(self, m):
        rest_events_view = api.content.create(
            container=self.portal,
            type="imio.smartweb.EventsView",
            title="Rest events view",
        )
        events = api.content.create(
            container=self.portalpage,
            type="imio.smartweb.SectionEvents",
            title="My events",
        )
        intids = getUtility(IIntIds)
        events.related_events = "e73e6a81afea4a579cd0da2773af8d29"
        events.linking_rest_view = RelationValue(intids.getId(rest_events_view))
        view = queryMultiAdapter((self.portalpage, self.request), name="full_view")
        self.assertIn("My events", view())
        events_view = queryMultiAdapter((events, self.request), name="carousel_view")
        self.assertEqual(events_view.items, [])
        url = "http://localhost:8080/Plone/@events?selected_agendas=e73e6a81afea4a579cd0da2773af8d29&metadata_fields=category_title&metadata_fields=start&metadata_fields=end&metadata_fields=has_leadimage&metadata_fields=image_scales&metadata_fields=UID&event_dates.query=2021-11-15&event_dates.range=min&b_size=6&translated_in_en=1&sort_on=event_dates"
        m.get(url, text=json.dumps(self.json_events))
        self.assertEqual(events_view.items[0][0].get("title"), "Journée de l'ATL")
        self.assertEqual(len(events_view.items[0]), 2)
        events.specific_related_events = ["1178188bddde4ced95a6cf8bf04c443c"]
        url = "http://localhost:8080/Plone/@events?UID=1178188bddde4ced95a6cf8bf04c443c&metadata_fields=category_title&metadata_fields=start&metadata_fields=end&metadata_fields=has_leadimage&metadata_fields=image_scales&metadata_fields=UID&event_dates.query=2021-11-15&event_dates.range=min&b_size=6&translated_in_en=1"
        m.get(url, text=json.dumps(self.json_specific_event))
        self.assertEqual(len(events_view.items[0]), 1)
        self.assertEqual(events_view.items[0][0].get("title"), "Bonne cheville")
