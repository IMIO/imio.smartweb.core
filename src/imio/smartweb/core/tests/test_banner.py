# -*- coding: utf-8 -*-

from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.viewlets.banner import BannerViewlet
from plone import api
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.namedfile.file import NamedBlobFile
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

    def test_viewlet_banner(self):
        viewlet = BannerViewlet(self.folder, self.request, None, None)
        viewlet.update()
        self.assertFalse(viewlet.available())
        self.folder.banner = NamedBlobFile(data="file data", filename=u"file.png")
        self.assertTrue(viewlet.available())
        self.assertIn(
            "background-image:url('http://nohost/plone/folder/@@images/banner/large')",
            viewlet.background_style(),
        )

    def test_no_banner(self):
        viewlet = BannerViewlet(self.folder, self.request, None, None)
        viewlet.update()
        self.assertFalse(viewlet.available())

    def test_banner_root_locally_hidden(self):
        self.folder.banner = NamedBlobFile(data="file data", filename=u"file.png")
        viewlet = BannerViewlet(self.folder, self.request, None, None)
        viewlet.update()
        self.assertTrue(viewlet.available())
        self.assertFalse(viewlet.is_banner_locally_hidden)
        switch_banner_display = getMultiAdapter(
            (self.folder, self.request), name="switch_banner_display"
        )
        switch_banner_display()
        self.assertTrue(viewlet.is_banner_locally_hidden)
        subfolder = api.content.create(
            container=self.folder,
            type="imio.smartweb.Folder",
            title="Subfolder",
        )
        subfolder_viewlet = BannerViewlet(subfolder, self.request, None, None)
        subfolder_viewlet.update()
        self.assertFalse(subfolder_viewlet.available())
        self.assertFalse(subfolder_viewlet.is_banner_locally_hidden)
        self.assertEqual(subfolder_viewlet.background_style(), "")

    def test_banner_child_locally_hidden(self):
        self.folder.banner = NamedBlobFile(data="file data", filename=u"file.png")
        viewlet = BannerViewlet(self.folder, self.request, None, None)
        viewlet.update()
        self.assertTrue(viewlet.available())
        subfolder = api.content.create(
            container=self.folder,
            type="imio.smartweb.Folder",
            title="Subfolder",
        )
        page = api.content.create(
            container=subfolder,
            type="imio.smartweb.Page",
            title="Page",
        )

        switch_banner_display = getMultiAdapter(
            (subfolder, self.request), name="switch_banner_display"
        )
        # Hide banner on subfolder
        switch_banner_display()
        subfolder_viewlet = BannerViewlet(subfolder, self.request, None, None)
        subfolder_viewlet.update()
        self.assertTrue(subfolder_viewlet.available())
        self.assertTrue(subfolder_viewlet.is_banner_locally_hidden)
        self.assertEqual(subfolder_viewlet.background_style(), "")
        page_viewlet = BannerViewlet(page, self.request, None, None)
        page_viewlet.update()
        self.assertFalse(page_viewlet.available())
        self.assertFalse(page_viewlet.is_banner_locally_hidden)
        self.assertEqual(page_viewlet.background_style(), "")

        # Show banner again on subfolder
        switch_banner_display()
        subfolder_viewlet = BannerViewlet(subfolder, self.request, None, None)
        subfolder_viewlet.update()
        self.assertTrue(subfolder_viewlet.available())
        self.assertFalse(subfolder_viewlet.is_banner_locally_hidden)
        self.assertIn(
            "background-image:url('http://nohost/plone/folder/@@images/banner/large')",
            subfolder_viewlet.background_style(),
        )
        page_viewlet = BannerViewlet(page, self.request, None, None)
        page_viewlet.update()
        self.assertTrue(page_viewlet.available())
        self.assertFalse(page_viewlet.is_banner_locally_hidden)
        self.assertIn(
            "background-image:url('http://nohost/plone/folder/@@images/banner/large')",
            page_viewlet.background_style(),
        )

    def test_banner_can_edit_locally_hidden(self):
        self.folder.banner = NamedBlobFile(data="file data", filename=u"file.png")
        viewlet = BannerViewlet(self.folder, self.request, None, None)
        viewlet.update()
        self.assertTrue(viewlet.available())
        subfolder = api.content.create(
            container=self.folder,
            type="imio.smartweb.Folder",
            title="Subfolder",
        )

        switch_banner_display = getMultiAdapter(
            (subfolder, self.request), name="switch_banner_display"
        )
        # Hide banner on subfolder
        switch_banner_display()
        subfolder_viewlet = BannerViewlet(subfolder, self.request, None, None)
        subfolder_viewlet.update()
        self.assertTrue(subfolder_viewlet.available())
        self.assertTrue(subfolder_viewlet.is_banner_locally_hidden)
        self.assertEqual(subfolder_viewlet.background_style(), "")
        logout()
        self.assertFalse(subfolder_viewlet.available())
