# -*- coding: utf-8 -*-

from imio.smartweb.core.viewlets.toolbar import AuthenticSourcesMenuItem
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import get_json
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.browsermenu.interfaces import IBrowserMenu
from zope.component import getUtility

import json
import requests_mock


class TestToolbar(ImioSmartwebTestCase):

    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests"""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.request = self.layer["request"]

    @requests_mock.Mocker()
    def test_sources_authentic_url(self, m):
        menu = getUtility(IBrowserMenu, name="plone_contentmenu", context=self.portal)
        m.get(
            "http://localhost:8080/Plone/@search?UID=7c69f9a738ec497c819725c55888ee32",
            text=json.dumps(get_json("resources/json_auth_sources_news_entity.json")),
        )
        m.get(
            "http://localhost:8080/Plone/@search?UID=7c69f9a738ec497c819725c55888ee31",
            text=json.dumps(get_json("resources/json_auth_sources_events_entity.json")),
        )
        m.get(
            "http://localhost:8080/Plone/@search?UID=396907b3b1b04a97896b12cc792c77f8",
            text=json.dumps(
                get_json("resources/json_auth_sources_directory_entity.json")
            ),
        )
        items = menu.getMenuItems(self.portal, self.request)
        authentic_sources_submenu = items[3].get("submenu")
        self.assertEqual(
            authentic_sources_submenu[0].get("title"),
            "localhost:8080/Plone/manage-news",
        )
        self.assertEqual(
            authentic_sources_submenu[1].get("title"),
            "localhost:8080/Plone/manage-events",
        )
        self.assertEqual(
            authentic_sources_submenu[2].get("title"),
            "localhost:8080/Plone/manage-directory",
        )

    def test_available(self):
        menu = AuthenticSourcesMenuItem(self.portal, self.request)
        self.assertTrue(menu.available())
        logout()
        self.assertFalse(menu.available())
