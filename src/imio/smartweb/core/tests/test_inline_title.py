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
from plone.protect.authenticator import createToken
from plone.testing.zope import Browser
from zope.component import getMultiAdapter

import transaction


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

    def test_title_is_editable_for_editors(self):
        for obj in (self.folder, self.page, self.section):
            rendered = getMultiAdapter((obj, self.request), name="inline_title")()
            self.assertIn('<span class="inline-title"', rendered)
            self.assertIn('contenteditable="true"', rendered)
            self.assertIn("{}/@@savetitle".format(obj.absolute_url()), rendered)
            self.assertIn(obj.Title(), rendered)

        # and it is really plugged into the headings the editor sees
        self.assertIn(
            '<h1><span class="inline-title"',
            getMultiAdapter((self.folder, self.request), name="title")(),
        )
        page_view = getMultiAdapter((self.page, self.request), name="full_view")()
        self.assertIn('<h1 class="page-title"><span class="inline-title"', page_view)
        self.assertIn('<h2 class="section-title"><span class="inline-title"', page_view)

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

    def test_anonymous_can_not_save_title(self):
        transaction.commit()
        browser = self.get_browser(authenticated=False)
        browser.raiseHttpErrors = False

        self.post_title(browser, self.section, "Hacked+title")
        self.assertIn("/login", browser.url)
        self.assertEqual(self.section.Title(), "My section")
