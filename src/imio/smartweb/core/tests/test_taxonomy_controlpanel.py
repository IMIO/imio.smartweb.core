# -*- coding: utf-8 -*-

from imio.smartweb.core.browser.taxonomy_controlpanel import SmartwebImportJson
from imio.smartweb.core.interfaces import IImioSmartwebCoreLayer
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import clear_ram_cache
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter
from Products.CMFCore.indexing import processQueue
from zope.interface import alsoProvides

import json


class TestTaxonomySettingsControlPanelForm(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        alsoProvides(self.request, IImioSmartwebCoreLayer)

    def available_actions(self):
        view = getMultiAdapter((self.portal, self.request), name="taxonomy-settings")
        view.update()
        return list(view.form_instance.actions.keys())

    def test_update_actions(self):
        setRoles(self.portal, TEST_USER_ID, ["Site Administrator"])
        actions = self.available_actions()
        self.assertIn("add-taxonomy", actions)
        self.assertNotIn("delete-taxonomy", actions)

        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.assertIn("delete-taxonomy", self.available_actions())


class TestSmartwebImportJson(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        alsoProvides(self.request, IImioSmartwebCoreLayer)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="My page",
            language="fr",
        )
        self.page.taxonomy_page_category = ["emploi"]
        self.page.reindexObject()
        processQueue()

    def tearDown(self):
        clear_ram_cache()

    def test___call__(self):
        """Saving the taxonomy editor gives the new label to the objects"""
        self.request.method = "POST"
        self.request["BODY"] = json.dumps(
            {
                "taxonomy": "collective.taxonomy.page_category",
                "languages": ["fr"],
                "tree": {
                    "subnodes": [
                        {"key": "emploi", "translations": {"fr": "Recrutement"}}
                    ]
                },
            }
        )
        view = getMultiAdapter((self.portal, self.request), name="taxonomy-import")
        self.assertIsInstance(view, SmartwebImportJson)
        view()
        found = [b.getObject() for b in api.content.find(SearchableText="Recrutement")]
        self.assertEqual(found, [self.page])
