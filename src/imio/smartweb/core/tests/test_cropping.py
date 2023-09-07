# -*- coding: utf-8 -*-

from imio.smartweb.common.interfaces import ICropping
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import get_sections_types
from imio.smartweb.core.tests.utils import make_named_image
from plone import api
from plone.app.imagecropping.interfaces import IImageCroppingUtils
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.namedfile.file import NamedBlobImage
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
        # footer cropping
        view = getMultiAdapter((self.portal, self.request), name="footer_settings")
        view.add_footer()
        footer = self.portal.listFolderContents(
            contentFilter={"portal_type": "imio.smartweb.Footer"}
        )[0]
        adapter = ICropping(footer, alternate=None)
        self.assertEqual([], adapter.get_scales("background_image", self.request))

        # minisite cropping
        view = getMultiAdapter((self.folder, self.request), name="minisite_settings")
        view.enable()
        adapter = ICropping(self.folder, alternate=None)
        self.assertEqual(
            ["liste", "vignette", "slide"], adapter.get_scales("image", self.request)
        )
        self.assertEqual([], adapter.get_scales("banner", self.request))
        self.assertEqual(["preview"], adapter.get_scales("logo", self.request))
        view.disable()

        # subsite cropping
        view = getMultiAdapter((self.folder, self.request), name="subsite_settings")
        view.enable()
        adapter = ICropping(self.folder, alternate=None)
        self.assertEqual(
            ["liste", "vignette", "slide"], adapter.get_scales("image", self.request)
        )
        self.assertEqual([], adapter.get_scales("banner", self.request))
        self.assertEqual(["preview"], adapter.get_scales("logo", self.request))
        view.disable()

        # folder cropping
        adapter = ICropping(self.folder, alternate=None)
        self.assertIsNotNone(adapter)
        self.assertEqual([], adapter.get_scales("banner", self.request))
        self.assertNotIn("banner", adapter.get_scales("image", self.request))

        # page cropping
        adapter = ICropping(self.page, alternate=None)
        self.assertEqual(
            ["liste", "vignette", "slide"], adapter.get_scales("image", self.request)
        )

        # sections cropping
        section_types = get_sections_types()
        for section_type in section_types:
            section = api.content.create(
                container=self.page,
                type=section_type,
                title="Title of my {}".format(section_type),
            )
            adapter = ICropping(section, alternate=None)
            self.assertIsNotNone(adapter)
            self.assertEqual([], adapter.get_scales("background_image", self.request))
            self.assertNotIn("banner", adapter.get_scales("image", self.request))

    def test_uncroppable_fields(self):
        self.folder.banner = NamedBlobImage(**make_named_image("plone.png"))
        self.folder.image = NamedBlobImage(**make_named_image("plone.png"))
        adapter = IImageCroppingUtils(self.folder, alternate=None)
        self.assertIsNotNone(adapter)
        self.assertEqual(len(list(adapter._image_field_values())), 1)
        self.assertEqual(adapter.image_field_names(), ["image"])

    def test_cropping_view(self):
        self.folder.banner = NamedBlobImage(**make_named_image("plone.png"))
        self.folder.image = NamedBlobImage(**make_named_image("plone.png"))
        cropping_view = getMultiAdapter(
            (self.folder, self.request), name="croppingeditor"
        )
        self.assertEqual(len(list(cropping_view._scales("banner"))), 0)
        self.assertEqual(len(list(cropping_view._scales("image"))), 3)
        self.assertNotIn("Banner", cropping_view())
        self.assertIn("Lead Image", cropping_view())
