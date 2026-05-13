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
from zope.schema.interfaces import IVocabularyFactory

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
        url = "http://localhost:8080/Plone/@events?selected_agendas=e73e6a81afea4a579cd0da2773af8d29&metadata_fields=container_uid&metadata_fields=category_title&metadata_fields=local_category&metadata_fields=topics&metadata_fields=start&metadata_fields=end&metadata_fields=has_leadimage&metadata_fields=modified&metadata_fields=UID&event_dates.query=2021-11-15&event_dates.range=min&b_size=6&translated_in_en=1&sort_on=event_dates"
        m.get(url, text=json.dumps(self.json_events))
        self.assertEqual(events_view.items[0][0].get("title"), "Journée de l'ATL")
        self.assertEqual(len(events_view.items[0]), 2)
        self.events.specific_related_events = ["1178188bddde4ced95a6cf8bf04c443c"]
        url = "http://localhost:8080/Plone/@events?UID=1178188bddde4ced95a6cf8bf04c443c&metadata_fields=container_uid&metadata_fields=category_title&metadata_fields=local_category&metadata_fields=topics&metadata_fields=start&metadata_fields=end&metadata_fields=has_leadimage&metadata_fields=modified&metadata_fields=UID&event_dates.query=2021-11-15&event_dates.range=min&b_size=6&translated_in_en=1"
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
        url = f"http://localhost:8080/Plone/@events?selected_agendas=e73e6a81afea4a579cd0da2773af8d29&metadata_fields=container_uid&metadata_fields=category_title&metadata_fields=local_category&metadata_fields=topics&metadata_fields=start&metadata_fields=end&metadata_fields=has_leadimage&metadata_fields=modified&metadata_fields=UID&event_dates.query={today_str}&event_dates.range=min&b_size=6&translated_in_en=1&sort_on=event_dates"
        m.get(url, text=json.dumps(self.json_events))
        self.assertEqual(len(events_view.items[0]), 2)
        hash_1 = annotations.get(SECTION_ITEMS_HASH_KEY)
        self.assertIsNotNone(hash_1)
        first_modification = self.portalpage.ModificationDate()

        sleep(1)
        url = f"http://localhost:8080/Plone/@events?selected_agendas=e73e6a81afea4a579cd0da2773af8d29&metadata_fields=container_uid&metadata_fields=category_title&metadata_fields=local_category&metadata_fields=topics&metadata_fields=start&metadata_fields=end&metadata_fields=has_leadimage&metadata_fields=modified&metadata_fields=UID&event_dates.query={today_str}&event_dates.range=min&b_size=6&translated_in_en=1&sort_on=event_dates"
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
        url = f"http://localhost:8080/Plone/@events?selected_agendas=e73e6a81afea4a579cd0da2773af8d29&metadata_fields=container_uid&metadata_fields=category_title&metadata_fields=local_category&metadata_fields=topics&metadata_fields=start&metadata_fields=end&metadata_fields=has_leadimage&metadata_fields=modified&metadata_fields=UID&event_dates.query={today_str}&event_dates.range=min&b_size=6&translated_in_en=1&sort_on=event_dates"
        m.get(url, text=json.dumps(self.json_events))

        self.assertIn("paysage_vignette", events_view.items[0][0]["image"])
        self.events.orientation = "portrait"
        self.assertIn("portrait_vignette", events_view.items[0][0]["image"])

    @requests_mock.Mocker()
    def test_show_categories_or_topics(self, m):
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
        url = f"http://localhost:8080/Plone/@events?selected_agendas=e73e6a81afea4a579cd0da2773af8d29&metadata_fields=container_uid&metadata_fields=category_title&metadata_fields=local_category&metadata_fields=topics&metadata_fields=start&metadata_fields=end&metadata_fields=has_leadimage&metadata_fields=modified&metadata_fields=UID&event_dates.query={today_str}&event_dates.range=min&b_size=6&translated_in_en=1&sort_on=event_dates"
        m.get(url, text=json.dumps(self.json_events))
        self.assertEqual(events_view.items[0][0]["category"], "Local Category title")
        self.assertEqual(events_view.items[0][1]["category"], "Presse")
        self.events.show_categories_or_topics = "category"
        self.assertEqual(events_view.items[0][0]["category"], "Local Category title")
        self.events.show_categories_or_topics = "topic"
        self.assertEqual(events_view.items[0][0]["category"], "Education")
        self.events.show_categories_or_topics = ""
        self.assertEqual(events_view.items[0][0]["category"], "")

    @requests_mock.Mocker()
    @freeze_time("2026-05-13")
    def test_whole_day_dates_converted_to_brussels_timezone(self, m):
        # Régression: un événement whole_day stocké comme 16/05 00:00→23:59
        # Bruxelles (= 15/05 22:00→16/05 21:59:59 UTC en CEST) s'affichait
        # "du 15/05 au 17/05" parce que view.py utilisait les datetimes UTC
        # bruts avec strftime('%d') dans macros.pt. Le rendu doit utiliser
        # le jour en TZ Europe/Brussels.
        intids = getUtility(IIntIds)
        self.events.related_events = "e73e6a81afea4a579cd0da2773af8d29"
        self.events.linking_rest_view = RelationValue(
            intids.getId(self.rest_events_view)
        )
        payload = {
            "items": [
                {
                    "@id": "http://localhost:8080/Plone/test-event",
                    "UID": "test-whole-day-uid",
                    "title": "Whole Day Event",
                    "description": "Test",
                    "start": "2026-05-15T22:00:00+00:00",
                    "end": "2026-05-16T21:59:59+00:00",
                    "modified": "2026-05-13T10:00:00+00:00",
                    "has_leadimage": False,
                }
            ]
        }
        m.get(
            requests_mock.ANY,
            text=json.dumps(payload),
        )
        events_view = queryMultiAdapter(
            (self.events, self.request), name="carousel_view"
        )
        item = events_view.items[0][0]
        start = item["event_date"]["start"]
        end = item["event_date"]["end"]
        # Bug si view.py ne fait pas astimezone(Europe/Brussels):
        # start.day == 15 (UTC) au lieu de 16 (Brussels)
        self.assertEqual(
            start.day,
            16,
            f"start.day doit être 16 en TZ Brussels, reçu {start.day} "
            f"(tzinfo={start.tzinfo}, raw={start.isoformat()})",
        )
        # Idem pour end: en UTC c'est 16/05 21:59:59, en Brussels 16/05 23:59:59
        self.assertEqual(end.day, 16)
        # is_multi_dates doit retourner False car les deux sont sur le 16/05
        # en TZ Brussels (donc macros.pt rend "On 16" et non "From 15 to 16").
        self.assertFalse(events_view.is_multi_dates(start, end))

    def test_linking_rest_view_vocabulary_is_site_wide(self):
        # Regression: a SectionEvents inside a minisite (INavigationRoot) must
        # accept a linking_rest_view pointing to an EventsView located outside
        # the minisite. With the navigation-root-scoped Catalog vocabulary
        # that was used before, validation raised ConstraintNotSatisfied.
        from imio.smartweb.core.behaviors.minisite import IImioSmartwebMinisite
        from zope.interface import alsoProvides

        minisite = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            id="minisite",
        )
        alsoProvides(minisite, IImioSmartwebMinisite)
        page = api.content.create(
            container=minisite,
            type="imio.smartweb.PortalPage",
            id="home",
        )
        section = api.content.create(
            container=page,
            type="imio.smartweb.SectionEvents",
            title="Section in minisite",
        )

        factory = getUtility(
            IVocabularyFactory, "imio.smartweb.vocabulary.EventsViewsSite"
        )
        vocabulary = factory(section)
        self.assertIn(api.content.get_uuid(self.rest_events_view), vocabulary)


# <audit>
#   <file>test_section_events.py</file>
#   <requirements_applied>R1, R2, R5, R6</requirements_applied>
#   <deviations>
#     test_whole_day_dates_converted_to_brussels_timezone teste view.items
#     (et non le HTML rendu) car le bug porte sur le datetime passé à
#     macros.pt; assertion sur start.day/end.day est suffisante et imite
#     le pattern des autres tests du fichier.
#   </deviations>
#   <questions>None</questions>
# </audit>
