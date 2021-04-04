# -*- coding: utf-8 -*-

from imio.smartweb.core.interfaces import IImioSmartwebSubsite
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.viewlets.subsite import SubsiteNavigationViewlet
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from zope.component import getMultiAdapter
import unittest


class SubsiteIntegrationTest(unittest.TestCase):

    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests"""
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            title="Folder",
            id="folder",
        )

    def test_activation(self):
        view = getMultiAdapter((self.portal, self.request), name="subsite_settings")
        self.assertFalse(view.available)

        view = getMultiAdapter((self.folder, self.request), name="subsite_settings")
        self.assertTrue(view.available)
        self.assertFalse(view.enabled)

        view.enable()
        self.assertTrue(IImioSmartwebSubsite.providedBy(self.folder))
        self.assertFalse(view.available)
        self.assertTrue(view.enabled)

        view.disable()
        self.assertFalse(IImioSmartwebSubsite.providedBy(self.folder))
        self.assertTrue(view.available)
        self.assertFalse(view.enabled)

    def test_viewlet(self):
        view = getMultiAdapter((self.folder, self.request), name="subsite_settings")
        view.enable()

        api.content.create(
            container=self.folder, type="imio.smartweb.Page", title="Page 1", id="page1"
        )
        subfolder = api.content.create(
            container=self.folder,
            type="imio.smartweb.Folder",
            title="Subfolder",
            id="subfolder",
        )

        viewlet = SubsiteNavigationViewlet(self.portal, self.request, None, None)
        viewlet.update()
        self.assertFalse(viewlet.available())

        viewlet = SubsiteNavigationViewlet(self.folder, self.request, None, None)
        viewlet.update()
        self.assertTrue(viewlet.available())
        items = viewlet.get_items()
        self.assertEqual(len(items["results"]), 2)

        viewlet = SubsiteNavigationViewlet(subfolder, self.request, None, None)
        viewlet.update()
        self.assertTrue(viewlet.available())
        self.assertEqual(viewlet.subsite_root, self.folder)
        items = viewlet.get_items()
        self.assertEqual(len(items["results"]), 2)
