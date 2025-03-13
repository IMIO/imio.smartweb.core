# -*- coding: utf-8 -*-

from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from unittest.mock import patch
from zope.component import queryMultiAdapter

import json


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
