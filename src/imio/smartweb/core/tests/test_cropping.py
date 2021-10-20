# -*- coding: utf-8 -*-

from imio.smartweb.common.interfaces import ICropping
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import get_leadimage_filename
from imio.smartweb.core.tests.utils import get_sections_types
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.namedfile.file import NamedBlobFile
from zope.component import getMultiAdapter


class TestCropping(ImioSmartwebTestCase):

    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

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
        self.page = api.content.create(
            container=self.folder,
            type="imio.smartweb.Page",
            title="Default Page",
            id="defaultpage",
        )

    def test_cropping_adapter(self):
        adapter = ICropping(self.folder, alternate=None)
        self.assertIsNotNone(adapter)
        self.assertEqual(["banner"], adapter.get_scales("banner", self.request))
        self.assertNotIn("banner", adapter.get_scales("image", self.request))
        section_types = get_sections_types()
        for section_type in section_types:
            section = api.content.create(
                container=self.page,
                type=section_type,
                title="Title of my {}".format(section_type),
            )
            adapter = ICropping(section, alternate=None)
            self.assertIsNotNone(adapter)
            self.assertIn("large", adapter.get_scales("background_image", self.request))
            self.assertNotIn("banner", adapter.get_scales("image", self.request))
            if section_type == "imio.smartweb.SectionText":
                self.assertEqual(
                    ["large"], adapter.get_scales("background_image", self.request)
                )
                section.image = NamedBlobFile(
                    "ploneLeadImage", filename=get_leadimage_filename()
                )
                section.image_size = "preview"
                self.assertEqual(["preview"], adapter.get_scales("image", self.request))

    def test_cropping_view(self):
        cropping_view = getMultiAdapter(
            (self.folder, self.request), name="croppingeditor"
        )
        self.assertEqual(len(list(cropping_view._scales("banner"))), 1)
        self.assertEqual(len(list(cropping_view._scales("image"))), 13)
        cropping_view = getMultiAdapter(
            (self.page, self.request), name="croppingeditor"
        )
        self.assertEqual(len(list(cropping_view._scales("image"))), 13)
        section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionText",
            title="Text section",
        )
        cropping_view = getMultiAdapter((section, self.request), name="croppingeditor")
        self.assertEqual(len(list(cropping_view._scales("image"))), 1)
