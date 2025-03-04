# -*- coding: utf-8 -*-

from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import make_named_image
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.namedfile.file import NamedBlobImage
from zope.component import queryMultiAdapter


class TestSectionGallery(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            id="page",
        )

    def test_alt_label(self):
        gallery_section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionGallery",
            title="Gallery section",
        )
        blob_image = NamedBlobImage(**make_named_image("plone.png"))

        # image1 has no defined title (by default img blob filename) and no description
        image1 = api.content.create(
            container=gallery_section,
            type="Image",
            title="plone.png",
        )
        image1.image = blob_image

        # image2 has a defined title and no description
        image2 = api.content.create(
            container=gallery_section,
            type="Image",
            title="Kamoulox",
        )
        image2.image = blob_image

        # image3 has a defined title and description (greater than title)
        image3 = api.content.create(
            container=gallery_section,
            type="Image",
            title="Hello Plone !",
        )
        image3.image = blob_image
        image3.description = "Hello Plone, what's up ?!"

        # image4 has a defined title and a mistaked blank description (smaller than title)
        image4 = api.content.create(
            container=gallery_section,
            type="Image",
            title="Hello Plone !",
        )
        # This is a mistaked blank description
        image4.image = blob_image
        image4.description = "  "

        view = queryMultiAdapter((gallery_section, self.request), name="view")
        self.assertEqual(view.alt_label(image1), "")
        self.assertEqual(view.alt_label(image2), "Kamoulox")
        self.assertEqual(view.alt_label(image3), "Hello Plone, what's up ?!")
        self.assertEqual(view.alt_label(image4), "Hello Plone !")
