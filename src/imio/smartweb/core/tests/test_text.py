# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from imio.smartweb.core.tests.utils import make_named_image
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.app.textfield.value import RichTextValue
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.namedfile.file import NamedBlobImage
from plone.protect.authenticator import createToken
from plone.testing.zope import Browser
from zope.component import getMultiAdapter

import json
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
        view = getMultiAdapter((self.page, self.request), name="full_view")
        self.assertIn(
            '<div class="body-section figure-left figure-section_text  no-image"',
            view(),
        )
        self.assertNotIn("<figure", view())
        self.assertNotIn("<figcaption", view())

        section.image = NamedBlobImage(**make_named_image())
        view = getMultiAdapter((self.page, self.request), name="full_view")
        self.assertIn(
            '<div class="body-section figure-left figure-section_text "', view()
        )
        self.assertIn("<figure", view())
        self.assertIn("@@images/image-760-", view())
        self.assertNotIn("<figcaption", view())

        section.image_caption = "Kamoulox"
        view = getMultiAdapter((self.page, self.request), name="full_view")
        # Assert section text has lead image
        self.assertIn(
            '<div class="body-section figure-left figure-section_text "', view()
        )
        self.assertIn("<figure", view())
        self.assertIn("figcaption", view())

        section.alignment = "right"
        view = getMultiAdapter((self.page, self.request), name="full_view")
        self.assertIn(
            '<div class="body-section figure-right figure-section_text "', view()
        )

        section.image_scale = "section_text_container"
        view = getMultiAdapter((self.page, self.request), name="full_view")
        self.assertIn(
            '<div class="body-section figure-right figure-section_text_container "',
            view(),
        )
        self.assertIn("@@images/image-1296-", view())

        # SVG images must not be scaled (PIL cannot process them)
        section.image = NamedBlobImage(**make_named_image("plone.svg"))
        view = getMultiAdapter((self.page, self.request), name="full_view")
        rendered = view()
        self.assertIn("<figure", rendered)
        self.assertIn("@@images/image?cache_key=", rendered)
        self.assertNotIn("@@images/image-", rendered)


class TestInlineEditView(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    def setUp(self):
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="Page",
        )
        self.section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionText",
            title="Title of my text",
        )
        self.section.text = RichTextValue("<p>Hello</p>", "text/html", "text/html")

    def get_textarea(self):
        view = getMultiAdapter((self.page, self.request), name="full_view")
        return BeautifulSoup(view(), "lxml").find("textarea", {"name": "newText"})

    def test_tinymce_options(self):
        textarea = self.get_textarea()
        self.assertIn("pat-tinymce", textarea["class"])
        options = json.loads(textarea["data-pat-tinymce"])
        # boxed editor (toolbar + height), not the chromeless "inline" mode
        self.assertFalse(options["inline"])
        self.assertEqual(options["tiny"]["height"], 500)

    def test_get_text(self):
        # TinyMCE reads the textarea when it starts, so the text has to be
        # rendered server side: an htmx swap would come too late
        self.assertEqual(self.get_textarea().text, "<p>Hello</p>")

    def test_can_edit(self):
        api.content.transition(self.page, "publish")
        logout()
        rendered = getMultiAdapter((self.page, self.request), name="full_view")()
        self.assertIn("<p>Hello</p>", rendered)
        self.assertNotIn("pat-tinymce", rendered)
        self.assertNotIn("handleDoubleClick", rendered)
        login(self.portal, TEST_USER_NAME)

    def test_save_text(self):
        transaction.commit()
        browser = Browser(self.layer["app"])
        browser.addHeader(
            "Authorization",
            "Basic %s:%s" % (TEST_USER_NAME, TEST_USER_PASSWORD),
        )
        browser.post(
            "{}/@@savetext".format(self.section.absolute_url()),
            "newText=%3Cp%3ENew+text%3C%2Fp%3E&_authenticator={}".format(createToken()),
            "application/x-www-form-urlencoded",
        )
        transaction.begin()
        # the response feeds the displayed div, so it is the rendered output
        self.assertEqual(browser.contents, "<p>New text</p>")
        self.assertEqual(self.section.text.raw, "<p>New text</p>")
