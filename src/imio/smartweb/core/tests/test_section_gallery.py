# -*- coding: utf-8 -*-

from imio.smartweb.common.config import DESCRIPTION_MAX_LENGTH
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import make_named_image
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.namedfile.file import NamedBlobImage
from plone.protect.authenticator import createToken
from Products.statusmessages.interfaces import IStatusMessage
from unittest.mock import patch
from zExceptions import Forbidden
from zope.component import queryMultiAdapter

DEDUCE_METADATA = "imio.omnia.core.services.OmniaCoreAPIService.deduce_metadata"


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

    def test_generate_images_description_button(self):
        gallery_section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionGallery",
            title="Gallery section",
        )
        view = queryMultiAdapter((self.page, self.request), name="full_view")
        self.assertNotIn("@@generate_images_description", view())

        image = api.content.create(
            container=gallery_section,
            type="Image",
            title="Image",
        )
        image.image = NamedBlobImage(**make_named_image("plone.png"))
        view = queryMultiAdapter((self.page, self.request), name="full_view")
        html = view()
        self.assertIn("@@generate_images_description?_authenticator=", html)
        self.assertNotIn("edit-section-images-described", html)

        image.description = "Une image"
        view = queryMultiAdapter((self.page, self.request), name="full_view")
        self.assertIn("edit-section-images-described", view())


class TestGenerateImagesDescriptionView(ImioSmartwebTestCase):
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
        self.gallery_section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionGallery",
            title="Gallery section",
        )

    def add_image(self, title, description="", with_blob=True):
        image = api.content.create(
            container=self.gallery_section,
            type="Image",
            title=title,
            description=description,
        )
        if with_blob:
            image.image = NamedBlobImage(**make_named_image("plone.png"))
        return image

    def call_view(self):
        self.request.form["_authenticator"] = createToken()
        view = queryMultiAdapter(
            (self.gallery_section, self.request), name="generate_images_description"
        )
        view()
        return [m.message for m in IStatusMessage(self.request).show()]

    def test_call(self):
        empty = self.add_image("Empty")
        blank = self.add_image("Blank", description="  ")
        described = self.add_image("Described", description="Kept by the editor")
        no_blob = self.add_image("No blob", with_blob=False)
        failing = self.add_image("Failing")

        with patch(
            DEDUCE_METADATA,
            side_effect=[
                {"title": "t", "description": "Une place communale.", "keywords": []},
                {"title": "t", "description": "Un  parc\n fleuri.", "keywords": []},
                Exception("Omnia is down"),
            ],
        ) as mock_deduce:
            messages = self.call_view()

        self.assertEqual(mock_deduce.call_count, 3)
        filename, data, content_type = mock_deduce.call_args_list[0].kwargs[
            "image_file"
        ]
        self.assertEqual(filename, "plone.png")
        self.assertEqual(data, empty.image.data)
        self.assertEqual(empty.description, "Une place communale.")
        self.assertEqual(blank.description, "Un parc fleuri.")
        self.assertEqual(described.description, "Kept by the editor")
        self.assertEqual(no_blob.description, "")
        self.assertEqual(failing.description, "")
        self.assertEqual(
            messages,
            [
                "2 image description(s) generated.",
                "1 image description(s) could not be generated.",
            ],
        )
        self.assertIn(
            f"#section-{self.gallery_section.id}",
            self.request.response.getHeader("location"),
        )

    def test_call_requires_authenticator(self):
        self.add_image("Empty")
        self.request.form["_authenticator"] = "wrong"
        view = queryMultiAdapter(
            (self.gallery_section, self.request), name="generate_images_description"
        )
        with patch(DEDUCE_METADATA) as mock_deduce:
            with self.assertRaises(Forbidden):
                view()
        mock_deduce.assert_not_called()

    def test_clean_description(self):
        view = queryMultiAdapter(
            (self.gallery_section, self.request), name="generate_images_description"
        )
        self.assertEqual(view._clean_description(None), "")
        self.assertEqual(view._clean_description(" a\n  b "), "a b")
        long_text = "mot " * 300
        cleaned = view._clean_description(long_text)
        self.assertLessEqual(len(cleaned), DESCRIPTION_MAX_LENGTH)
        self.assertTrue(cleaned.endswith("mot"))
