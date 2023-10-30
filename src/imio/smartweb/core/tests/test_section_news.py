# -*- coding: utf-8 -*-

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


class TestSectionNews(ImioSmartwebTestCase):
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
        self.json_news = get_json("resources/json_rest_news.json")
        self.json_specific_news = get_json("resources/json_rest_specific_news.json")
        self.rest_news_view = api.content.create(
            container=self.portal,
            type="imio.smartweb.NewsView",
            title="Rest news view",
        )
        self.news = api.content.create(
            container=self.portalpage,
            type="imio.smartweb.SectionNews",
            title="My news",
        )

    @requests_mock.Mocker()
    def test_news(self, m):
        intids = getUtility(IIntIds)
        self.news.related_news = "64f4cbee9a394a018a951f6d94452914"
        self.news.linking_rest_view = RelationValue(intids.getId(self.rest_news_view))
        self.news.link_text = "Voir toutes les actualités"
        view = queryMultiAdapter((self.portalpage, self.request), name="full_view")
        self.assertIn("My news", view())
        news_view = queryMultiAdapter((self.news, self.request), name="carousel_view")
        self.assertEqual(news_view.items, [])
        url = "http://localhost:8080/Plone/@search?selected_news_folders=64f4cbee9a394a018a951f6d94452914&portal_type=imio.news.NewsItem&metadata_fields=category_title&metadata_fields=has_leadimage&metadata_fields=modified&metadata_fields=effective&metadata_fields=UID&sort_limit=6&translated_in_en=1&sort_on=effective&sort_order=descending"
        m.get(url, text=json.dumps(self.json_news))
        self.assertEqual(news_view.items[0][0].get("title"), "Première actualité")
        self.assertEqual(len(news_view.items[0]), 3)

        self.news.specific_related_newsitems = [
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            "bfe2b4391a0f4a8db6d8b7fed63d1c4a",
        ]
        url = "http://localhost:8080/Plone/@search?UID=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa&UID=bfe2b4391a0f4a8db6d8b7fed63d1c4a&portal_type=imio.news.NewsItem&metadata_fields=category_title&metadata_fields=has_leadimage&metadata_fields=modified&metadata_fields=effective&metadata_fields=UID&sort_limit=6&translated_in_en=1"
        m.get(url, text=json.dumps(self.json_specific_news))
        self.assertEqual(len(news_view.items[0]), 2)
        self.assertEqual(
            news_view.items[0][0].get("title"), "Restauration de la piscine"
        )

        self.news.specific_related_newsitems = [
            "bfe2b4391a0f4a8db6d8b7fed63d1c4a",
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        ]
        m.get(url, text=json.dumps(self.json_specific_news))
        self.assertEqual(
            news_view.items[0][0].get("title"), "Restauration de la Bibliothèque"
        )

    @requests_mock.Mocker()
    def test_news_modified(self, m):
        intids = getUtility(IIntIds)
        self.news.related_news = "64f4cbee9a394a018a951f6d94452914"
        self.news.linking_rest_view = RelationValue(intids.getId(self.rest_news_view))
        annotations = IAnnotations(self.news)
        self.assertIsNone(annotations.get(SECTION_ITEMS_HASH_KEY))

        news_view = queryMultiAdapter((self.news, self.request), name="carousel_view")
        url = "http://localhost:8080/Plone/@search?selected_news_folders=64f4cbee9a394a018a951f6d94452914&portal_type=imio.news.NewsItem&metadata_fields=category_title&metadata_fields=has_leadimage&metadata_fields=modified&metadata_fields=effective&metadata_fields=UID&sort_limit=6&translated_in_en=1&sort_on=effective&sort_order=descending"
        m.get(url, text=json.dumps(self.json_news))
        self.assertEqual(len(news_view.items[0]), 3)
        hash_1 = annotations.get(SECTION_ITEMS_HASH_KEY)
        self.assertIsNotNone(hash_1)
        first_modification = self.portalpage.ModificationDate()

        sleep(1)
        url = "http://localhost:8080/Plone/@search?selected_news_folders=64f4cbee9a394a018a951f6d94452914&portal_type=imio.news.NewsItem&metadata_fields=category_title&metadata_fields=has_leadimage&metadata_fields=modified&metadata_fields=effective&metadata_fields=UID&sort_limit=6&translated_in_en=1&sort_on=effective&sort_order=descending"
        m.get(url, text="{}")
        self.assertEqual(len(news_view.items), 0)
        next_modification = self.portalpage.ModificationDate()
        hash_2 = annotations.get(SECTION_ITEMS_HASH_KEY)
        self.assertNotEqual(hash_1, hash_2)
        self.assertNotEqual(first_modification, next_modification)

        sleep(1)
        self.assertEqual(len(news_view.items), 0)
        last_modification = self.portalpage.ModificationDate()
        hash_3 = annotations.get(SECTION_ITEMS_HASH_KEY)
        self.assertEqual(hash_2, hash_3)
        self.assertEqual(next_modification, last_modification)

    @requests_mock.Mocker()
    def test_orientation(self, m):
        intids = getUtility(IIntIds)
        self.news.related_news = "64f4cbee9a394a018a951f6d94452914"
        self.news.linking_rest_view = RelationValue(intids.getId(self.rest_news_view))
        annotations = IAnnotations(self.news)
        self.assertIsNone(annotations.get(SECTION_ITEMS_HASH_KEY))

        news_view = queryMultiAdapter((self.news, self.request), name="carousel_view")
        url = "http://localhost:8080/Plone/@search?selected_news_folders=64f4cbee9a394a018a951f6d94452914&portal_type=imio.news.NewsItem&metadata_fields=category_title&metadata_fields=has_leadimage&metadata_fields=modified&metadata_fields=effective&metadata_fields=UID&sort_limit=6&translated_in_en=1&sort_on=effective&sort_order=descending"
        m.get(url, text=json.dumps(self.json_news))

        self.assertIn("paysage_vignette", news_view.items[0][0]["image"])
        self.news.orientation = "portrait"
        self.assertIn("portrait_vignette", news_view.items[0][0]["image"])
