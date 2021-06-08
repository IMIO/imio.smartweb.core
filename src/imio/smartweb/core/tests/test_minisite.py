# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from imio.smartweb.core.behaviors.minisite import IImioSmartwebMinisite
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import setRoles
from plone.dexterity.content import ASSIGNABLE_CACHE_KEY
from plone.testing.zope import Browser
from zope.component import getMultiAdapter

import transaction


class MinisiteFunctionalTest(ImioSmartwebTestCase):

    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    def setUp(self):
        """Custom shared utility setup for tests"""
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            title="Folder",
            id="folder",
        )
        # avoid cached empty value for instance behaviors
        delattr(self.request, ASSIGNABLE_CACHE_KEY)

    def test_activation(self):
        view = getMultiAdapter((self.portal, self.request), name="minisite_settings")
        self.assertFalse(view.available)

        view = getMultiAdapter((self.folder, self.request), name="minisite_settings")
        self.assertTrue(view.available)
        self.assertFalse(view.enabled)

        view.enable()
        self.assertTrue(IImioSmartwebMinisite.providedBy(self.folder))
        self.assertTrue(INavigationRoot.providedBy(self.folder))

        self.assertFalse(view.available)
        self.assertTrue(view.enabled)

        view.disable()
        self.assertFalse(IImioSmartwebMinisite.providedBy(self.folder))
        self.assertFalse(INavigationRoot.providedBy(self.folder))
        self.assertTrue(view.available)
        self.assertFalse(view.enabled)

        subsite_view = getMultiAdapter(
            (self.folder, self.request), name="subsite_settings"
        )
        subsite_view.enable()
        self.assertFalse(view.available)

    def test_minisite_exclude_from_nav(self):
        view = getMultiAdapter((self.folder, self.request), name="minisite_settings")
        view.enable()
        self.assertTrue(IImioSmartwebMinisite.providedBy(self.folder))
        self.assertTrue(self.folder.exclude_from_nav)

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
        soup = BeautifulSoup(content)
        exclude_from_nav_widget = soup.find(
            id="form-widgets-IExcludeFromNavigation-exclude_from_nav"
        )
        self.assertIsNone(exclude_from_nav_widget.find("input"))
        children = [
            c for c in exclude_from_nav_widget if not isinstance(c, str) or c.strip()
        ]
        self.assertEqual(len(children), 1)
        self.assertEqual(children[0].text, "yes")

    def test_move_minisite_in_folder(self):
        view = getMultiAdapter((self.folder, self.request), name="minisite_settings")
        view.enable()
        folder2 = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            title="Folder2",
            id="folder2",
        )
        moved_folder = api.content.move(self.folder, folder2)
        view = getMultiAdapter((moved_folder, self.request), name="minisite_settings")
        self.assertFalse(view.available)
        self.assertFalse(view.enabled)
        self.assertFalse(IImioSmartwebMinisite.providedBy(moved_folder))

    def test_copy_minisite_in_folder(self):
        view = getMultiAdapter((self.folder, self.request), name="minisite_settings")
        view.enable()
        folder2 = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            title="Folder2",
            id="folder2",
        )
        copied_folder = api.content.copy(self.folder, folder2)
        view = getMultiAdapter((copied_folder, self.request), name="minisite_settings")
        self.assertFalse(view.available)
        self.assertFalse(view.enabled)
        self.assertFalse(IImioSmartwebMinisite.providedBy(copied_folder))

    def test_minisite_in_minisite(self):
        view = getMultiAdapter((self.folder, self.request), name="minisite_settings")
        view.enable()
        self.assertTrue(IImioSmartwebMinisite.providedBy(self.folder))

        minisite2 = api.content.create(
            container=self.folder,
            type="imio.smartweb.Folder",
            title="minisite2",
            id="minisite2",
        )
        view = getMultiAdapter((minisite2, self.request), name="minisite_settings")
        self.assertFalse(view.available)
