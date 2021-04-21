# -*- coding: utf-8 -*-

from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.viewlets.banner import BannerViewlet
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.namedfile.file import NamedBlobFile
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
