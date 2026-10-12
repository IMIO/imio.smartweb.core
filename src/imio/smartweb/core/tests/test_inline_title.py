# -*- coding: utf-8 -*-

from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.locking.interfaces import ILockable
from plone.protect.authenticator import createToken
from plone.testing.zope import Browser
from zope.component import getMultiAdapter

import transaction
import unittest

INLINE_EDIT_DISABLED_REASON = (
    "inline edition is disabled for now (can_edit_content() short-circuits to"
    " False, see utils.py) - un-skip once it's re-enabled"
)


class InlineTitleTestCase(ImioSmartwebTestCase):
    """A folder holding a page holding a section: the 3 titles made editable"""

    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            title="My folder",
        )
        self.page = api.content.create(
            container=self.folder,
            type="imio.smartweb.Page",
            title="My page",
        )
        self.section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionText",
            title="My section",
        )

    def get_browser(self, authenticated=True):
        browser = Browser(self.layer["app"])
        if authenticated:
            browser.addHeader(
                "Authorization",
                "Basic %s:%s" % (TEST_USER_NAME, TEST_USER_PASSWORD),
            )
        return browser


class TestInlineTitleView(InlineTitleTestCase):

    @unittest.skip(INLINE_EDIT_DISABLED_REASON)
    def test_title_is_editable_for_editors(self):
        for obj in (self.folder, self.page, self.section):
            rendered = getMultiAdapter((obj, self.request), name="inline_title")()
            self.assertIn('<span class="inline-title"', rendered)
            self.assertIn('contenteditable="true"', rendered)
            self.assertIn("{}/@@savetitle".format(obj.absolute_url()), rendered)
            # so the front-end JS can lock the object (plone.locking) as
            # soon as the title gains focus, before the first @@savetitle
            # on blur
            self.assertIn(
                "{}/@@plone_lock_operations/create_lock".format(obj.absolute_url()),
                rendered,
            )
            self.assertIn(obj.Title(), rendered)

        # and it is really plugged into the headings the editor sees
        self.assertIn(
            '<h1><span class="inline-title"',
            getMultiAdapter((self.folder, self.request), name="title")(),
        )
        page_view = getMultiAdapter((self.page, self.request), name="full_view")()
        self.assertIn('<h1 class="page-title"><span class="inline-title"', page_view)
        self.assertIn('<h2 class="section-title"><span class="inline-title"', page_view)

    def test_title_is_plain_text_when_locked_by_other(self):
        # Someone else has this exact object open in the standard edit form
        # (plone.locking) - the contenteditable must not be mounted, same
        # as for a user without edit permission.
        ILockable(self.section).lock()
        login(self.portal, "test")
        rendered = getMultiAdapter((self.section, self.request), name="inline_title")()
        self.assertEqual(rendered, self.section.Title())
        login(self.portal, TEST_USER_NAME)

    @unittest.skip(INLINE_EDIT_DISABLED_REASON)
    def test_title_is_editable_for_lock_owner(self):
        # The editor holding the lock can keep editing normally.
        ILockable(self.section).lock()
        rendered = getMultiAdapter((self.section, self.request), name="inline_title")()
        self.assertIn('contenteditable="true"', rendered)

    def test_title_is_plain_text_for_anonymous(self):
        api.content.transition(self.folder, "publish")
        api.content.transition(self.page, "publish")
        logout()
        for obj in (self.folder, self.page, self.section):
            rendered = getMultiAdapter((obj, self.request), name="inline_title")()
            self.assertEqual(rendered, obj.Title())

        # public markup stays exactly what it was before inline edition
        self.assertEqual(
            getMultiAdapter((self.folder, self.request), name="title")().strip(),
            "<h1>My folder</h1>",
        )
        page_view = getMultiAdapter((self.page, self.request), name="full_view")()
        self.assertIn('<h1 class="page-title">My page</h1>', page_view)
        self.assertIn('<h2 class="section-title">My section</h2>', page_view)
        self.assertNotIn("inline-title", page_view)
        login(self.portal, TEST_USER_NAME)


class TestSaveTitleView(InlineTitleTestCase):

    def post_title(self, browser, obj, title, token=None):
        if token is None:
            token = createToken()
        browser.post(
            "{}/@@savetitle".format(obj.absolute_url()),
            "newTitle={}&_authenticator={}".format(title, token),
            "application/x-www-form-urlencoded",
        )
        transaction.begin()
        return browser.contents

    @unittest.skip(INLINE_EDIT_DISABLED_REASON)
    def test_save_title(self):
        transaction.commit()
        browser = self.get_browser()

        for obj in (self.folder, self.page, self.section):
            new_title = "Renamed {}".format(obj.portal_type)
            response = self.post_title(browser, obj, new_title.replace(" ", "+"))
            self.assertEqual(response, new_title)
            self.assertEqual(obj.Title(), new_title)
            # catalog follows, so listings and navigation show the new title
            brain = api.content.find(UID=obj.UID())[0]
            self.assertEqual(brain.Title, new_title)

        # surrounding whitespace of a contenteditable is dropped
        self.post_title(browser, self.section, "++Trimmed+title++")
        self.assertEqual(self.section.Title(), "Trimmed title")

        # an empty title is ignored: a content never loses its title
        self.post_title(browser, self.section, "+++")
        self.assertEqual(self.section.Title(), "Trimmed title")

        # blur/save also releases the lock focus had acquired
        self.assertFalse(ILockable(self.section).locked())

    @unittest.skip(INLINE_EDIT_DISABLED_REASON)
    def test_lock_on_focus_then_save_releases_it(self):
        # simulates the real front-end sequence: focus locks the object,
        # then blur saves and releases the lock.
        transaction.commit()
        browser = self.get_browser()

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

        response = self.post_title(browser, self.section, "Renamed+section")
        self.assertEqual(response, "Renamed section")
        self.assertEqual(self.section.Title(), "Renamed section")
        self.assertFalse(ILockable(self.section).locked())

    def test_save_title_refused_when_locked_by_other(self):
        ILockable(self.section).lock()
        login(self.portal, "test")
        self.request.form["newTitle"] = "Hacked title"
        self.request.form["_authenticator"] = createToken()
        view = getMultiAdapter((self.section, self.request), name="savetitle")
        result = view()
        # unchanged: the write was silently ignored
        self.assertEqual(result, "My section")
        self.assertEqual(self.section.Title(), "My section")
        login(self.portal, TEST_USER_NAME)

    def test_anonymous_can_not_save_title(self):
        transaction.commit()
        browser = self.get_browser(authenticated=False)
        browser.raiseHttpErrors = False

        self.post_title(browser, self.section, "Hacked+title")
        self.assertIn("/login", browser.url)
        self.assertEqual(self.section.Title(), "My section")
