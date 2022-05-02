# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from imio.smartweb.core.tests.utils import make_named_image
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.namedfile.file import NamedBlobImage
from plone.testing.zope import Browser
from zope.component import getMultiAdapter

import transaction


class TestText(ImioSmartwebTestCase):

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

    def test_toggle_title_visibility(self):
        page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="Page",
        )
        api.content.transition(page, "publish")
        # We can't edit title visibility of a "Text" section.
        # And visibility of text title is False.
        section = api.content.create(
            container=page,
            type="imio.smartweb.SectionText",
            title="Title of my text",
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

    def test_lead_image(self):
        section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionText",
            title="Title of my text",
        )
        section.alignment = "left"
        section.image_size = "large"
        view = getMultiAdapter((self.page, self.request), name="full_view")
        self.assertIn(
            '<div class="body-section figure-left figure-large  no-image"', view()
        )
        self.assertNotIn("<figure", view())
        self.assertNotIn("@@images/image/large", view())
        self.assertNotIn("figcaption", view())

        section.image = NamedBlobImage(**make_named_image())
        view = getMultiAdapter((self.page, self.request), name="full_view")
        self.assertIn('<div class="body-section figure-left figure-large "', view())
        self.assertIn("<figure", view())
        self.assertIn("@@images/image/large", view())
        self.assertNotIn("figcaption", view())

        section.image_caption = "Kamoulox"
        view = getMultiAdapter((self.page, self.request), name="full_view")
        # Assert section text has lead image
        self.assertIn('<div class="body-section figure-left figure-large "', view())
        self.assertIn("<figure", view())
        self.assertIn("figcaption", view())

        section.alignment = "right"
        view = getMultiAdapter((self.page, self.request), name="full_view")
        self.assertIn('<div class="body-section figure-right figure-large "', view())

        section.image_size = "mini"
        view = getMultiAdapter((self.page, self.request), name="full_view")
        self.assertIn('<div class="body-section figure-right figure-mini "', view())
        self.assertIn("@@images/image/mini", view())
