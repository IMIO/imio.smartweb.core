# -*- coding: utf-8 -*-

from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import get_json
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import queryMultiAdapter

import json
import requests
import requests_mock


class SectionsIntegrationTest(ImioSmartwebTestCase):

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
        self.json_contact = get_json("resources/json_contact_raw_mock.json")
        self.json_no_contact = get_json("resources/json_no_contact_raw_mock.json")
        self.json_contact_images = get_json(
            "resources/json_contact_images_raw_mock.json"
        )
        self.json_no_image = get_json("resources/json_contact_no_image_raw_mock.json")

    @requests_mock.Mocker()
    def test_contact(self, m):
        m.get(
            "http://localhost:8080/Plone/2dc381f0fb584381b8e4a19c84f53b35/@search?portal_type=Image&path.depth=1",
            text=json.dumps(self.json_contact_images),
        )
        contact = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionContact",
            title="My contact",
        )
        view = queryMultiAdapter((self.page, self.request), name="full_view")
        self.assertIn("My contact", view())
        contact_view = queryMultiAdapter((contact, self.request), name="view")
        self.assertIsNone(contact_view.contact)
        contact.related_contact = "2dc381f0fb584381b8e4a19c84f53b35"
        m.get(
            "http://localhost:8080/Plone/@search?UID=2dc381f0fb584381b8e4a19c84f53b35&fullobjects=1",
            exc=requests.exceptions.ConnectTimeout,
        )
        self.assertIsNone(contact_view.contact)
        m.get(
            "http://localhost:8080/Plone/@search?UID=2dc381f0fb584381b8e4a19c84f53b35&fullobjects=1",
            status_code=404,
        )
        self.assertIsNone(contact_view.contact)
        m.get(
            "http://localhost:8080/Plone/@search?UID=2dc381f0fb584381b8e4a19c84f53b35&fullobjects=1",
            text=json.dumps(self.json_no_contact),
        )
        self.assertIsNone(contact_view.contact)
        m.get(
            "http://localhost:8080/Plone/@search?UID=2dc381f0fb584381b8e4a19c84f53b35&fullobjects=1",
            text=json.dumps(self.json_contact),
        )
        self.assertIsNotNone(contact_view.contact)
        self.assertNotIn("contact_titles", view())
        self.assertIn("contact_address", view())
        self.assertIn("contact_informations", view())
        # self.assertIn("schedule", view())
        self.assertNotIn("contact_gallery", view())
        contact.visible_blocks = ["titles", "gallery"]
        self.assertIn("contact_titles", view())
        self.assertNotIn("contact_address", view())
        self.assertNotIn("contact_informations", view())
        # self.assertNotIn("schedule", view())

        self.assertIn("contact_gallery", view())
        self.assertEqual(len(contact_view.images), 2)
        m.get(
            "http://localhost:8080/Plone/2dc381f0fb584381b8e4a19c84f53b35/@search?portal_type=Image&path.depth=1",
            text=json.dumps(self.json_no_image),
        )
        self.assertIsNone(contact_view.images)
        m.get(
            "http://localhost:8080/Plone/2dc381f0fb584381b8e4a19c84f53b35/@search?portal_type=Image&path.depth=1",
            status_code=404,
        )
        self.assertIsNone(contact_view.images)
        m.get(
            "http://localhost:8080/Plone/2dc381f0fb584381b8e4a19c84f53b35/@search?portal_type=Image&path.depth=1",
            exc=requests.exceptions.ConnectTimeout,
        )
        self.assertIsNone(contact_view.images)
