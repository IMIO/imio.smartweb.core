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
from plone.locking.interfaces import ILockable
from plone.namedfile.file import NamedBlobImage
from plone.protect.authenticator import createToken
from plone.testing.zope import Browser
from zope.component import getMultiAdapter

import json
import transaction
import unittest

INLINE_EDIT_DISABLED_REASON = (
    "inline edition is disabled for now (can_edit_content() short-circuits to"
    " False, see utils.py) - un-skip once it's re-enabled"
)


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

    @unittest.skip(INLINE_EDIT_DISABLED_REASON)
    def test_tinymce_options(self):
        textarea = self.get_textarea()
        self.assertIn("pat-tinymce", textarea["class"])
        options = json.loads(textarea["data-pat-tinymce"])
        # chromeless "inline" mode: no permanent toolbar/menu/status bar,
        # just a text cursor, and a small "quickbars" toolbar on selection
        self.assertTrue(options["inline"])
        self.assertFalse(options["tiny"]["toolbar"])
        self.assertFalse(options["tiny"]["menubar"])
        self.assertFalse(options["tiny"]["statusbar"])
        self.assertIn("quickbars", options["tiny"]["plugins"])
        self.assertIn("lists", options["tiny"]["plugins"])
        toolbar = options["tiny"]["quickbars_selection_toolbar"]
        self.assertIn("plonelink", toolbar)
        self.assertIn("underline", toolbar)
        # heading levels for content paragraphs: h3+ only, h1/h2 are
        # reserved for the page/section titles themselves
        self.assertIn("h3", toolbar)
        self.assertIn("h4", toolbar)
        self.assertIn("h5", toolbar)
        self.assertNotIn("h1", toolbar)
        self.assertNotIn("h2", toolbar)
        self.assertIn("bullist", toolbar)
        self.assertIn("numlist", toolbar)
        # Omnia AI assistant (imio.omnia.tinymce), installed site-wide
        self.assertIn("omnia", toolbar)
        # no iframe in inline mode: don't inject the theme's content_css
        # (meant for the boxed editor's iframe) into the page's own <head>
        self.assertFalse(options["tiny"]["content_css"])

    @unittest.skip(INLINE_EDIT_DISABLED_REASON)
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
        self.assertNotIn("inline-text-edit", rendered)
        login(self.portal, TEST_USER_NAME)

    @unittest.skip(INLINE_EDIT_DISABLED_REASON)
    def test_lock_url_attribute(self):
        # so the front-end JS can lock the section (plone.locking) as soon
        # as TinyMCE gains focus, before the first @@savetext on blur
        view = getMultiAdapter((self.page, self.request), name="full_view")
        form = BeautifulSoup(view(), "lxml").find("form", {"class": "inline-text-edit"})
        self.assertEqual(
            form["data-lock-url"],
            "{}/@@plone_lock_operations/create_lock".format(
                self.section.absolute_url()
            ),
        )

    @unittest.skip(INLINE_EDIT_DISABLED_REASON)
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
        # blur/save also releases the lock focus had acquired
        self.assertFalse(ILockable(self.section).locked())

    @unittest.skip(INLINE_EDIT_DISABLED_REASON)
    def test_lock_on_focus_then_save_releases_it(self):
        # simulates the real front-end sequence: TinyMCE "focus" locks the
        # section, then "blur" saves and releases the lock.
        transaction.commit()
        browser = Browser(self.layer["app"])
        browser.addHeader(
            "Authorization",
            "Basic %s:%s" % (TEST_USER_NAME, TEST_USER_PASSWORD),
        )
        browser.post(
            "{}/@@plone_lock_operations/create_lock".format(
                self.section.absolute_url()
            ),
            "redirect:boolean=false",
            "application/x-www-form-urlencoded",
        )
        transaction.begin()
        self.assertTrue(ILockable(self.section).locked())
        self.assertTrue(ILockable(self.section).can_safely_unlock())

        browser.post(
            "{}/@@savetext".format(self.section.absolute_url()),
            "newText=%3Cp%3ENew+text%3C%2Fp%3E&_authenticator={}".format(createToken()),
            "application/x-www-form-urlencoded",
        )
        transaction.begin()
        self.assertEqual(self.section.text.raw, "<p>New text</p>")
        self.assertFalse(ILockable(self.section).locked())

    def test_lock_status_banner_shown_to_other_editor(self):
        # once someone else's inline edition has really locked the section
        # (plone.locking), the standard "#plone-lock-status" banner
        # (SectionView.locking_info, already wired in section_edition)
        # must show up for a second editor.
        ILockable(self.section).lock()
        login(self.portal, "test")
        rendered = getMultiAdapter((self.page, self.request), name="full_view")()
        soup = BeautifulSoup(rendered, "lxml")
        # the page's own (unlocked) #plone-lock-status from the standard
        # plone.lockinfo viewlet is also on the page, hence find_all: we
        # only care that the section's own banner (rendered inline, via
        # SectionView.locking_info) is among them and shows "Locked".
        banners = soup.find_all(id="plone-lock-status")
        self.assertTrue(banners)
        self.assertTrue(any("Locked" in banner.get_text() for banner in banners))
        login(self.portal, TEST_USER_NAME)

    def test_can_edit_false_when_locked_by_other(self):
        # Someone else has this exact section open in the standard edit
        # form (plone.locking) - the chromeless inline TinyMCE editor must
        # not be mounted, same as for a user without edit permission.
        ILockable(self.section).lock()
        login(self.portal, "test")
        rendered = getMultiAdapter((self.page, self.request), name="full_view")()
        self.assertIn("<p>Hello</p>", rendered)
        self.assertNotIn("pat-tinymce", rendered)
        self.assertNotIn("inline-text-edit", rendered)
        login(self.portal, TEST_USER_NAME)

    @unittest.skip(INLINE_EDIT_DISABLED_REASON)
    def test_can_edit_true_for_lock_owner(self):
        # The editor holding the lock can keep editing normally.
        ILockable(self.section).lock()
        view = getMultiAdapter((self.section, self.request), name="view")
        self.assertTrue(view.can_edit())

    def test_save_text_refused_when_locked_by_other(self):
        ILockable(self.section).lock()
        login(self.portal, "test")
        self.request.form["newText"] = "<p>Hacked</p>"
        self.request.form["_authenticator"] = createToken()
        view = getMultiAdapter((self.section, self.request), name="view")
        result = view.save_text()
        # unchanged: the write was silently ignored
        self.assertEqual(result, "<p>Hello</p>")
        self.assertEqual(self.section.text.raw, "<p>Hello</p>")
        login(self.portal, TEST_USER_NAME)
