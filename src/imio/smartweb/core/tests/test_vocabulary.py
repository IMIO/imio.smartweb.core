# -*- coding: utf-8 -*-

from imio.smartweb.core import config
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import mock_entity_newsfolders
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from unittest.mock import patch
from zope.component import queryMultiAdapter

import json
import re
import requests_mock


class TestVocabulary(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests"""
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="My Page",
        )

    def test_getvocabulary(self):
        self.request.form = {
            "name": "imio.smartweb.vocabulary.Topics",
            "field": "topics",
        }
        view = queryMultiAdapter((self.page, self.request), name="getVocabulary")
        result = json.loads(view())
        self.assertEqual(result["results"][0]["id"], "entertainment")
        self.assertEqual(result["results"][0]["text"], "Entertainment")
        with patch("plone.api.portal.get_current_language", return_value="fr"):
            view = queryMultiAdapter((self.page, self.request), name="getVocabulary")
            result = json.loads(view())
            self.assertEqual(result["results"][0]["id"], "entertainment")
            self.assertEqual(
                result["results"][0]["text"], "Activités et divertissement"
            )

        self.page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="My Page",
        )
        self.contacts = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionContact",
            title="My contancts",
        )
        self.request.form = {
            "name": "imio.smartweb.vocabulary.RemoteContacts",
            "field": "related_contacts",
        }
        view = queryMultiAdapter((self.contacts, self.request), name="getVocabulary")
        result = json.loads(view())
        self.assertEqual(result["results"], [])

    @requests_mock.Mocker()
    def test_getvocabulary_batches_a_filtered_remote_vocabulary(self, m):
        # select2 sends batch={"page": n, "size": pageSize} and asks for the
        # next page while pageSize * page < total, so the response must carry
        # the *unbatched* total -- reporting len(results) stopped it after one
        # page and forced this view to return everything at once.
        mock_entity_newsfolders(m)
        m.get(
            re.compile(
                re.escape(config.NEWS_URL) + r"/@search\?selected_news_folders="
            ),
            text=json.dumps(
                {
                    "items": [
                        {"UID": f"uid-{i}", "breadcrumb": f"Belleville » Actu {i}"}
                        for i in range(25)
                    ]
                }
            ),
        )
        portalpage = api.content.create(
            container=self.portal,
            type="imio.smartweb.PortalPage",
            title="Portal page",
        )
        section = api.content.create(
            container=portalpage,
            type="imio.smartweb.SectionNews",
            title="My news",
        )
        self.request.form = {
            "name": "imio.smartweb.vocabulary.NewsItemsFromEntity",
            "field": "specific_related_newsitems",
            "batch": json.dumps({"page": 1, "size": 10}),
        }
        view = queryMultiAdapter((section, self.request), name="getVocabulary")
        result = json.loads(view())
        self.assertEqual(len(result["results"]), 10)
        self.assertEqual(result["total"], 25)
        self.assertEqual(result["results"][0]["id"], "uid-0")

        # page 2 continues where page 1 stopped
        self.request.form["batch"] = json.dumps({"page": 2, "size": 10})
        view = queryMultiAdapter((section, self.request), name="getVocabulary")
        result = json.loads(view())
        self.assertEqual(result["results"][0]["id"], "uid-10")
        self.assertEqual(result["total"], 25)

        # the total stays the size of what the *query* matches, not of the page
        self.request.form["query"] = "Actu 1"
        self.request.form["batch"] = json.dumps({"page": 1, "size": 10})
        view = queryMultiAdapter((section, self.request), name="getVocabulary")
        result = json.loads(view())
        # "Actu 1" matches 1 and 10-19
        self.assertEqual(result["total"], 11)
        self.assertEqual(len(result["results"]), 10)

    @requests_mock.Mocker()
    def test_getvocabulary_caps_an_unbatched_request(self, m):
        # a caller that sends no batch parameter gets one page, not the entity
        mock_entity_newsfolders(m)
        m.get(
            re.compile(
                re.escape(config.NEWS_URL) + r"/@search\?selected_news_folders="
            ),
            text=json.dumps(
                {
                    "items": [
                        {"UID": f"uid-{i}", "breadcrumb": f"Actu {i}"}
                        for i in range(120)
                    ]
                }
            ),
        )
        portalpage = api.content.create(
            container=self.portal,
            type="imio.smartweb.PortalPage",
            title="Portal page",
        )
        section = api.content.create(
            container=portalpage,
            type="imio.smartweb.SectionNews",
            title="My news",
        )
        self.request.form = {
            "name": "imio.smartweb.vocabulary.NewsItemsFromEntity",
            "field": "specific_related_newsitems",
        }
        view = queryMultiAdapter((section, self.request), name="getVocabulary")
        result = json.loads(view())
        self.assertEqual(len(result["results"]), 50)
        self.assertEqual(result["total"], 120)
