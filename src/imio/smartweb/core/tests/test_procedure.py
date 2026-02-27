# -*- coding: utf-8 -*-
from imio.smartweb.core.contents import IProcedure
from imio.smartweb.core.contents.pages.views import PagesView
from imio.smartweb.core.tests.utils import get_json
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.utils import populate_procedure_button_text
from imio.smartweb.core.viewlets.procedure import ProcedureViewlet
from plone import api
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.z3cform.interfaces import IPloneFormLayer
from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryMultiAdapter
from zope.component import queryUtility
from zope.interface import alsoProvides
from zope.publisher.browser import TestRequest
from zope.viewlet.interfaces import IViewletManager

import json
import requests_mock

# formdefs/
GUICHET_URL = "https://demo.guichet-citoyen.be/api/"
WCS_URL = "https://demo-formulaires.guichet-citoyen.be/api/"


class TestProcedure(ImioSmartwebTestCase):
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
        self.json_procedures_raw_mock = get_json(
            "resources/json_procedures_raw_mock.json"
        )

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
            "IProcedure not provided by {0}!".format(
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
            "IProcedure not provided by {0}!".format(
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
        self.assertTrue(fti.global_allow, "{0} is globally addable!".format(fti.id))

    @requests_mock.Mocker()
    def test_procedure_invariant(self, m):
        url = f"{WCS_URL}formdefs/"
        m.get(url, text=json.dumps(self.json_procedures_raw_mock))
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
        self.assertTrue(len(errors) == 0)

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

    @requests_mock.Mocker()
    def test_procedure_viewlet(self, m):
        url = f"{WCS_URL}formdefs/"
        m.get(url, text=json.dumps(self.json_procedures_raw_mock))
        procedure = api.content.create(
            container=self.portal,
            type="imio.smartweb.Procedure",
            id="procedure",
        )

        view = PagesView(self.portal["procedure"], self.request)
        manager_name = "plone.abovecontentbody"

        manager = queryMultiAdapter(
            (self.portal["procedure"], self.request, view),
            IViewletManager,
            manager_name,
            default=None,
        )
        manager.update()
        viewlet = [
            v for v in manager.viewlets if v.__name__ == "imio.smartweb.procedure"
        ]
        self.assertEqual(len(viewlet), 1)
        self.assertEqual("", viewlet[0]().strip())
        url = "http://another_e_guichet.be/procedure1"
        procedure.procedure_url = url
        self.assertIn(url, viewlet[0]())
        procedure.procedure_url = None
        procedure.procedure_ts = (
            "https://demo-formulaires.guichet-citoyen.be/acte-de-deces/"
        )
        self.assertIn("Acte de d\\u00e9c\\u00e8s", viewlet[0]())


class TestProcedureViewletMethods(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.json_procedures_raw_mock = get_json(
            "resources/json_procedures_raw_mock.json"
        )
        self.procedure = api.content.create(
            container=self.portal,
            type="imio.smartweb.Procedure",
            id="test-procedure",
        )

    def _make_viewlet(self):
        view = PagesView(self.procedure, self.request)
        viewlet = ProcedureViewlet(self.procedure, self.request, view, None)
        viewlet.update()
        return viewlet

    # --- get_selected_procedure_title ---

    def test_get_selected_procedure_title_none_when_no_procedure_ts(self):
        self.procedure.procedure_ts = None
        viewlet = self._make_viewlet()
        self.assertIsNone(viewlet.get_selected_procedure_title())

    @requests_mock.Mocker()
    def test_get_selected_procedure_title_returns_term_when_set(self, m):
        url = f"{WCS_URL}formdefs/"
        m.get(url, text=json.dumps(self.json_procedures_raw_mock))
        self.procedure.procedure_ts = (
            "https://demo-formulaires.guichet-citoyen.be/acte-de-deces/"
        )
        viewlet = self._make_viewlet()
        term = viewlet.get_selected_procedure_title()
        self.assertIsNotNone(term)
        self.assertIn("Acte de d\\u00e9c\\u00e8s", term.title)

    # --- is_anonymous ---

    def test_is_anonymous_returns_false_when_authenticated(self):
        login(self.portal, "test")
        viewlet = self._make_viewlet()
        self.assertFalse(viewlet.is_anonymous)

    def test_is_anonymous_returns_true_when_anonymous(self):
        logout()
        viewlet = self._make_viewlet()
        self.assertTrue(viewlet.is_anonymous)
        login(self.portal, "test")

    # --- get_button_label ---

    def test_get_button_label_default_when_button_ts_label_is_none(self):
        self.procedure.button_ts_label = None
        viewlet = self._make_viewlet()
        self.assertEqual(viewlet.get_button_label(), "Complete this procedure online")

    def test_get_button_label_returns_term_title_when_valid_label(self):
        populate_procedure_button_text()
        self.procedure.button_ts_label = "label-2"
        viewlet = self._make_viewlet()
        self.assertEqual(viewlet.get_button_label(), "Apply")

    def test_get_button_label_default_when_unknown_token(self):
        populate_procedure_button_text()
        self.procedure.button_ts_label = "nonexistent-label"
        viewlet = self._make_viewlet()
        self.assertEqual(viewlet.get_button_label(), "Complete this procedure online")
