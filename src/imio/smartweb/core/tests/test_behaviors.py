# -*- coding: utf-8 -*-
from imio.smartweb.core.behaviors.procedure import IProcedure  # NOQA E501
from imio.smartweb.core.contents import IProcedure  # NOQA E501
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING  # noqa
from imio.smartweb.core.tests.utils import get_procedure_json
from plone import api
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from plone.testing.z2 import Browser
from zope.component import createObject
from zope.component import queryUtility

import json
import os
import requests_mock
import transaction
import unittest


class ProcedureFunctionalTest(unittest.TestCase):

    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    def _changeUser(self, loginName):
        logout()
        login(self.portal, loginName)
        self.member = api.user.get_current()
        self.request["AUTHENTICATED_USER"] = self.member

    def setUp(self):
        app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self._changeUser("test")
        self.json_procedures_raw_mock = get_procedure_json()

        # Set up browser
        self.browser = Browser(app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            "Authorization",
            "Basic {username}:{password}".format(
                username=SITE_OWNER_NAME, password=SITE_OWNER_PASSWORD
            ),
        )

    @requests_mock.Mocker()
    def test_procedure_invariant(self, m):
        folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            id="folder",
        )
        transaction.commit()
        m.get(
            "https://demo.guichet-citoyen.be/api/formdefs/",
            text=json.dumps(self.json_procedures_raw_mock),
        )
        self.browser.open(folder.absolute_url() + "/++add++imio.smartweb.Procedure")
        self.browser.getControl("Save").click()
        self.assertIn("Procedure field is required !", self.browser.contents)

        self.browser.getControl(name="form.widgets.IBasic.title").value = "My Procedure"
        self.browser.getControl(
            name="form.widgets.IProcedure.procedure_url"
        ).value = "http://another_e_guichet.be/procedure1"
        self.browser.getControl(
            name="form.widgets.IProcedure.procedure_ts:list"
        ).value = "https://demo-formulaires.guichet-citoyen.be/acte-de-deces/"
        self.browser.getControl("Save").click()
        self.assertIn("Only one procedure field can be filled !", self.browser.contents)

        self.browser.getControl(name="form.widgets.IProcedure.procedure_url").value = ""
        self.browser.getControl("Save").click()
        self.assertIn(
            '<h1 class="documentFirstHeading">My Procedure</h1>', self.browser.contents
        )
