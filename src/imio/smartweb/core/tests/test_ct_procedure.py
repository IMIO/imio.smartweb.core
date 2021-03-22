# -*- coding: utf-8 -*-
from imio.smartweb.core.contents import IProcedure  # NOQA E501
from imio.smartweb.core.tests.utils import get_procedure_json
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.z3cform.interfaces import IPloneFormLayer
from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility
from zope.interface import alsoProvides
from zope.publisher.browser import TestRequest

import json
import requests_mock
import unittest


class ProcedureIntegrationTest(unittest.TestCase):

    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def _changeUser(self, loginName):
        logout()
        login(self.portal, loginName)
        self.member = api.user.get_current()
        self.request["AUTHENTICATED_USER"] = self.member

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            "imio.smartweb.Folder",
            self.portal,
            "parent_container",
            title="Parent container",
        )
        self.parent = self.portal[parent_id]
        self._changeUser("test")
        self.json_procedures_raw_mock = get_procedure_json()

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

    @requests_mock.Mocker()
    def test_procedure_invariant(self, m):
        m.get(
            "https://demo.guichet-citoyen.be/api/formdefs/",
            text=json.dumps(self.json_procedures_raw_mock),
        )
        request = TestRequest(
            form={
                "form.widgets.IBasic.title": "My Procedure",
                "form.widgets.procedure_url": "http://another_e_guichet.be/procedure1",
            }
        )
        alsoProvides(request, IPloneFormLayer)
        form = DefaultAddForm(self.portal, request)
        form.portal_type = "imio.smartweb.Procedure"
        form.update()
        data, errors = form.extractData()
        self.assertTrue(len(errors) == 0)

        request = TestRequest(
            form={
                "form.widgets.IBasic.title": "My Procedure",
            }
        )
        alsoProvides(request, IPloneFormLayer)
        form = DefaultAddForm(self.portal, request)
        form.portal_type = "imio.smartweb.Procedure"
        form.update()
        data, errors = form.extractData()
        self.assertTrue(len(errors) == 1)
        self.assertIn(errors[0].message, "Procedure field is required !")

        request = TestRequest(
            form={
                "form.widgets.IBasic.title": "My Procedure",
                "form.widgets.procedure_url": "http://another_e_guichet.be/procedure1",
                "form.widgets.procedure_ts": "https://demo-formulaires.guichet-citoyen.be/acte-de-deces/",
            }
        )
        alsoProvides(request, IPloneFormLayer)
        form = DefaultAddForm(self.portal, request)
        form.portal_type = "imio.smartweb.Procedure"
        form.update()
        data, errors = form.extractData()
        self.assertTrue(len(errors) == 1)
        self.assertIn(errors[0].message, "Only one procedure field can be filled !")
