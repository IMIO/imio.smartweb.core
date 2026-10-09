# -*- coding: utf-8 -*-

from imio.smartweb.core.rest.eguichet import KIMUG_AUTHENTICATED_ROLE
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_ACCEPTANCE_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession
from unittest import mock

import os
import transaction

ENVIRON = {"RESTAPI_USER_USERNAME": "sw-user", "RESTAPI_USER_PASSWORD": "sw-pwd"}


class TestEguichetApiSettingsGet(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_ACCEPTANCE_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        if KIMUG_AUTHENTICATED_ROLE not in self.portal.validRoles():
            self.portal._addRole(KIMUG_AUTHENTICATED_ROLE)
        api.user.create(
            email="member@imio.be", username="member", password="secret-pwd"
        )
        api.user.create(email="sso@imio.be", username="sso", password="secret-pwd")
        api.user.grant_roles(username="sso", roles=[KIMUG_AUTHENTICATED_ROLE])
        transaction.commit()
        self.api_session = RelativeSession(self.portal.absolute_url())
        self.api_session.headers.update({"Accept": "application/json"})

    def tearDown(self):
        self.api_session.close()
        api.user.delete(username="member")
        api.user.delete(username="sso")
        transaction.commit()

    @mock.patch.dict(os.environ, ENVIRON)
    def test_reply(self):
        # Anonymous and simple members can not read the settings
        response = self.api_session.get("@eguichet-api-settings")
        self.assertEqual(response.status_code, 401)
        self.api_session.auth = ("member", "secret-pwd")
        response = self.api_session.get("@eguichet-api-settings")
        self.assertEqual(response.status_code, 401)

        expected = {
            "url_ts": "https://demo.guichet-citoyen.be/api",
            "wcs_api_url": "https://demo-formulaires.guichet-citoyen.be/api",
            "username": "sw-user",
            "password": "sw-pwd",
        }
        # SSO technical users and Managers can read the settings
        self.api_session.auth = ("sso", "secret-pwd")
        response = self.api_session.get("@eguichet-api-settings")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        response = self.api_session.get("@eguichet-api-settings")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)
