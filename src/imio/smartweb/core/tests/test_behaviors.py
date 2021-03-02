# -*- coding: utf-8 -*-
from imio.smartweb.core.behaviors.procedure import IProcedure  # NOQA E501
from imio.smartweb.core.browser.procedure.add import AddForm
from imio.smartweb.core.contents import IProcedure  # NOQA E501
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING  # noqa
from imio.smartweb.core.tests.utils import get_procedure_json
from plone import api
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.z3cform.interfaces import IPloneFormLayer
from zope.interface import alsoProvides
from zope.publisher.browser import TestRequest

import json
import requests_mock
import unittest


class ProcedureFunctionalTest(unittest.TestCase):

    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    def _changeUser(self, loginName):
        logout()
        login(self.portal, loginName)
        self.member = api.user.get_current()
        self.request["AUTHENTICATED_USER"] = self.member

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self._changeUser("test")
        self.json_procedures_raw_mock = get_procedure_json()

    @requests_mock.Mocker()
    def test_procedure_invariant(self, m):
        m.get(
            "https://demo.guichet-citoyen.be/api/formdefs/",
            text=json.dumps(self.json_procedures_raw_mock),
        )
        request = TestRequest(
            form={
                "form.widgets.IBasic.title": "My Procedure",
                "form.widgets.IProcedure.procedure_url": "http://another_e_guichet.be/procedure1",
            }
        )
        alsoProvides(request, IPloneFormLayer)
        form = AddForm(self.portal, request)
        form.update()
        data, errors = form.extractData()
        self.assertTrue(len(errors) == 0)

        request = TestRequest(
            form={
                "form.widgets.IBasic.title": "My Procedure",
            }
        )
        alsoProvides(request, IPloneFormLayer)
        form = AddForm(self.portal, request)
        form.update()
        data, errors = form.extractData()
        self.assertTrue(len(errors) == 1)
        self.assertIn(errors[0].message, "Procedure field is required !")

        request = TestRequest(
            form={
                "form.widgets.IBasic.title": "My Procedure",
                "form.widgets.IProcedure.procedure_url": "http://another_e_guichet.be/procedure1",
                "form.widgets.IProcedure.procedure_ts": "https://demo-formulaires.guichet-citoyen.be/acte-de-deces/",
            }
        )
        alsoProvides(request, IPloneFormLayer)
        form = AddForm(self.portal, request)
        form.update()
        data, errors = form.extractData()
        self.assertTrue(len(errors) == 1)
        self.assertIn(errors[0].message, "Only one procedure field can be filled !")

    def test_quick_access(self):
        page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="Quick access page",
            include_in_quick_access=True,
        )
        brains = api.content.find(include_in_quick_access=True)
        self.assertEquals(len(brains), 1)
        self.assertEquals(page, brains[0].getObject())
        page.include_in_quick_access = False
        page.reindexObject()
        brains = api.content.find(include_in_quick_access=True)
        self.assertEquals(len(brains), 0)
