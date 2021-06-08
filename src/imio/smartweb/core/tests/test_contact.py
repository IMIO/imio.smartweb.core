# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import get_json
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.zope import Browser
from zope.component import queryMultiAdapter

import json
import requests
import requests_mock
import transaction


class SectionsFunctionalTest(ImioSmartwebTestCase):

    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

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
        contact = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionContact",
            title="My contact",
        )
        view = queryMultiAdapter((self.page, self.request), name="full_view")
        self.assertIn("My contact", view())
        contact_view = queryMultiAdapter((contact, self.request), name="view")
        self.assertIsNone(contact_view.contact)
        authentic_contact_uid = "2dc381f0fb584381b8e4a19c84f53b35"
        contact.related_contact = authentic_contact_uid
        contact_search_url = (
            "http://localhost:8080/Plone/@search?UID={}&fullobjects=1".format(
                authentic_contact_uid
            )
        )
        contact_images_url = "http://localhost:8080/Plone/{}/@search?portal_type=Image&path.depth=1".format(
            authentic_contact_uid
        )
        m.get(contact_search_url, exc=requests.exceptions.ConnectTimeout)
        self.assertIsNone(contact_view.contact)
        m.get(contact_search_url, status_code=404)
        self.assertIsNone(contact_view.contact)
        m.get(contact_search_url, text=json.dumps(self.json_no_contact))
        self.assertIsNone(contact_view.contact)
        m.get(contact_search_url, text=json.dumps(self.json_contact))
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

        m.get(contact_images_url, text=json.dumps(self.json_contact_images))
        self.assertIn("contact_gallery", view())
        self.assertEqual(len(contact_view.images), 2)

        m.get(contact_search_url, exc=requests.exceptions.ConnectTimeout)
        self.assertIsNone(contact_view.images)
        m.get(contact_search_url, status_code=404)
        self.assertIsNone(contact_view.images)
        m.get(contact_search_url, text=json.dumps(self.json_no_contact))
        self.assertIsNone(contact_view.images)

        m.get(contact_search_url, text=json.dumps(self.json_contact))
        m.get(contact_images_url, text=json.dumps(self.json_no_image))
        self.assertIsNone(contact_view.images)
        m.get(contact_images_url, status_code=404)
        self.assertIsNone(contact_view.images)
        m.get(contact_images_url, exc=requests.exceptions.ConnectTimeout)
        self.assertIsNone(contact_view.images)

    def test_toggle_title_visibility(self):
        page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="Page",
        )
        api.content.transition(page, "publish")
        # We can't edit title visibility of a "Contact" section.
        # And visibility of contact title is False.
        section = api.content.create(
            container=page,
            type="imio.smartweb.SectionContact",
            title="Title of my contact",
        )
        transaction.commit()
        browser = Browser(self.layer["app"])
        browser.addHeader(
            "Authorization",
            "Basic %s:%s"
            % (
                TEST_USER_NAME,
                TEST_USER_PASSWORD,
            ),
        )
        browser.open("{}/edit".format(section.absolute_url()))
        content = browser.contents
        soup = BeautifulSoup(content)
        hide_title_true = soup.find(id="form-widgets-hide_title-0")
        self.assertIsNotNone(hide_title_true)
        self.assertEqual(len(hide_title_true), 0)
        self.assertEqual(hide_title_true["type"], "hidden")
        self.assertEqual(hide_title_true["value"], "selected")
        hide_title_false = soup.find(id="form-widgets-hide_title-1")
        self.assertIsNone(hide_title_false)

        browser.open("{}/++add++{}".format(page.absolute_url(), section.portal_type))
        content = browser.contents
        soup = BeautifulSoup(content)
        hide_title_true = soup.find(id="form-widgets-hide_title-0")
        self.assertIsNotNone(hide_title_true)
        self.assertEqual(len(hide_title_true), 0)
        self.assertEqual(hide_title_true["type"], "hidden")
        self.assertEqual(hide_title_true["value"], "selected")
        hide_title_false = soup.find(id="form-widgets-hide_title-1")
        self.assertIsNone(hide_title_false)
