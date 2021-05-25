# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.zope import Browser
import transaction
import unittest


class FormsFunctionalTest(unittest.TestCase):

    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    def setUp(self):
        """Custom shared utility setup for tests"""
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_leadimage_caption_field(self):
        container = self.portal
        folder = api.content.create(
            container=container,
            type="imio.smartweb.Folder",
            title="My folder",
        )
        self.check_leadimage_caption_field(folder, container=container)

        container = folder
        page = api.content.create(
            container=container,
            type="imio.smartweb.Page",
            title="My page",
        )
        self.check_leadimage_caption_field(page, container=container)

        procedure = api.content.create(
            container=container,
            type="imio.smartweb.Procedure",
            title="My page",
        )
        self.check_leadimage_caption_field(procedure, container=container)

    def check_leadimage_caption_field(self, obj, container):
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
        browser.open("{}/edit".format(obj.absolute_url()))
        content = browser.contents
        soup = BeautifulSoup(content)
        lead_image_caption_widget = soup.find(
            id="form-widgets-ILeadImageBehavior-image_caption"
        )
        self.assertIsNotNone(lead_image_caption_widget)
        self.assertEqual(len(lead_image_caption_widget), 0)
        self.assertEqual(lead_image_caption_widget["type"], "hidden")

        browser.open("{}/++add++{}".format(container.absolute_url(), obj.portal_type))
        content = browser.contents
        soup = BeautifulSoup(content)
        lead_image_caption_widget = soup.find(
            id="form-widgets-ILeadImageBehavior-image_caption"
        )
        self.assertIsNotNone(lead_image_caption_widget)
        self.assertEqual(len(lead_image_caption_widget), 0)
        self.assertEqual(lead_image_caption_widget["type"], "hidden")
