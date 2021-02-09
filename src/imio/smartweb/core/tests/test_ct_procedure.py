# -*- coding: utf-8 -*-
from imio.smartweb.core.contents import IProcedure  # NOQA E501
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import json
import requests_mock
import unittest


class ProcedureIntegrationTest(unittest.TestCase):

    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            "imio.smartweb.Folder",
            self.portal,
            "parent_container",
            title="Parent container",
        )
        self.parent = self.portal[parent_id]

    def test_ct_procedure_schema(self):
        fti = queryUtility(IDexterityFTI, name="imio.smartweb.Procedure")
        schema = fti.lookupSchema()
        self.assertEqual(IProcedure, schema)

    def test_ct_procedure_fti(self):
        fti = queryUtility(IDexterityFTI, name="imio.smartweb.Procedure")
        self.assertTrue(fti)

    def test_ct_procedure_factory(self):
        fti = queryUtility(IDexterityFTI, name="imio.smartweb.Procedure")
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IProcedure.providedBy(obj),
            u"IProcedure not provided by {0}!".format(
                obj,
            ),
        )

    def test_ct_procedure_adding(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        obj = api.content.create(
            container=self.parent,
            type="imio.smartweb.Procedure",
            id="procedure",
        )

        self.assertTrue(
            IProcedure.providedBy(obj),
            u"IProcedure not provided by {0}!".format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn("procedure", parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn("procedure", parent.objectIds())

    def test_ct_procedure_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        fti = queryUtility(IDexterityFTI, name="imio.smartweb.Procedure")
        self.assertTrue(fti.global_allow, u"{0} is globally addable!".format(fti.id))
