# -*- coding: utf-8 -*-

from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.app.multilingual import api as api_lng
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.testing.zope import Browser
from Products.CMFPlone.utils import get_installer

import transaction


class TestRedirectToMainReactView(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    def setUp(self):
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        installer = get_installer(self.portal, self.layer["request"])
        installer.install_product("plone.app.multilingual")
        self.rest_directory = api.content.create(
            container=self.portal,
            type="imio.smartweb.DirectoryView",
            title="directory view",
        )
        self.rest_agenda = api.content.create(
            container=self.portal,
            type="imio.smartweb.EventsView",
            title="agenda view",
        )
        self.rest_news = api.content.create(
            container=self.portal,
            type="imio.smartweb.NewsView",
            title="news view",
        )
        api.content.transition(self.rest_directory, "publish")
        api.content.transition(self.rest_agenda, "publish")
        api.content.transition(self.rest_news, "publish")

    def test_rest_view_redirection(self):

        folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            id="folder",
        )
        rest_views = {
            "directory": self.rest_directory,
            "events": self.rest_agenda,
            "news": self.rest_news,
        }
        browser = Browser(self.layer["app"])
        for k, v in rest_views.items():
            api.portal.set_registry_record(f"smartweb.default_{k}_view", v.UID())
            transaction.commit()
            rest_view_url = v.absolute_url()
            browser.open(f"{self.portal_url}/@@{k}_view")
            self.assertEqual(browser.url, rest_view_url)

            v = api.content.move(v, folder)
            transaction.commit()
            rest_view_url = v.absolute_url()
            browser.open(f"{self.portal_url}/@@{k}_view")
            self.assertEqual(browser.url, rest_view_url)

            obj = api_lng.translate(v, target_language="de")
            api.content.transition(obj, "publish")
            transaction.commit()
            browser.open(f"{self.portal_url}/@@{k}_view?language=de")
            self.assertEqual(browser.url, obj.absolute_url())

            api.content.delete(v)
            transaction.commit()
            browser.open(f"{self.portal_url}/@@{k}_view")
            self.assertEqual(browser.url, self.portal_url)
