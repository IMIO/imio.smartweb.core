# -*- coding: utf-8 -*-

from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.zope import Browser
from zope.component import getMultiAdapter

import transaction


class TestLocalRoles(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    def setUp(self):
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            title="Folder",
        )
        self.page = api.content.create(
            container=self.folder,
            type="imio.smartweb.Page",
            title="Page",
        )

    def test_local_manager_in_sharing(self):
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
        browser.open("{}/@@sharing".format(self.folder.absolute_url()))
        content = browser.contents
        self.assertNotIn("Can manage locally", content)

        view = getMultiAdapter((self.folder, self.request), name="minisite_settings")
        view.enable()
        transaction.commit()
        browser.open("{}/@@sharing".format(self.folder.absolute_url()))
        content = browser.contents
        self.assertIn("Can manage locally", content)

    def test_local_manager_for_minisite_logo(self):
        view = getMultiAdapter((self.folder, self.request), name="minisite_settings")
        view.enable()
        setRoles(
            self.portal, TEST_USER_ID, ["Reader", "Editor", "Contributor", "Reviewer"]
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
        browser.open("{}/edit".format(self.folder.absolute_url()))
        content = browser.contents
        self.assertNotIn(
            '"formfield-form-widgets-IImioSmartwebMinisiteSettings-logo"', content
        )

        self.folder.manage_setLocalRoles(TEST_USER_ID, ("Local Manager",))
        transaction.commit()
        browser.open("{}/edit".format(self.folder.absolute_url()))
        content = browser.contents
        self.assertIn(
            '"formfield-form-widgets-IImioSmartwebMinisiteSettings-logo"', content
        )

    def test_local_manager_for_new_html_section(self):
        view = getMultiAdapter((self.folder, self.request), name="minisite_settings")
        view.enable()
        setRoles(
            self.portal, TEST_USER_ID, ["Reader", "Editor", "Contributor", "Reviewer"]
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
        browser.open("{}".format(self.page.absolute_url()))
        content = browser.contents
        self.assertNotIn("++add++imio.smartweb.SectionHTML", content)

        self.folder.manage_setLocalRoles(TEST_USER_ID, ("Local Manager",))
        transaction.commit()
        browser.open("{}".format(self.page.absolute_url()))
        content = browser.contents
        self.assertIn("++add++imio.smartweb.SectionHTML", content)

    def test_local_manager_for_existing_html_section(self):
        section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionHTML",
            title="Section",
        )
        view = getMultiAdapter((self.folder, self.request), name="minisite_settings")
        view.enable()
        setRoles(
            self.portal, TEST_USER_ID, ["Reader", "Editor", "Contributor", "Reviewer"]
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
        self.assertNotIn("formfield-form-widgets-html", content)

        self.folder.manage_setLocalRoles(TEST_USER_ID, ("Local Manager",))
        transaction.commit()
        browser.open("{}/edit".format(section.absolute_url()))
        content = browser.contents
        self.assertIn("formfield-form-widgets-html", content)
