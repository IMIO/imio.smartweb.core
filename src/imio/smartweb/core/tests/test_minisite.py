# -*- coding: utf-8 -*-

from imio.smartweb.core.browser.minisite.settings import IImioSmartwebMinisite
from imio.smartweb.core.behaviors.subsite import IImioSmartwebSubsite
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.dexterity.content import ASSIGNABLE_CACHE_KEY
from zope.component import getMultiAdapter


class MinisiteIntegrationTest(ImioSmartwebTestCase):

    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

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
        self.assertTrue(IImioSmartwebSubsite.providedBy(self.folder))
        self.assertTrue(IImioSmartwebMinisite.providedBy(self.folder))
        self.assertTrue(INavigationRoot.providedBy(self.folder))

        self.assertFalse(view.available)
        self.assertTrue(view.enabled)

        view.disable()
        self.assertFalse(IImioSmartwebSubsite.providedBy(self.folder))
        self.assertFalse(IImioSmartwebMinisite.providedBy(self.folder))
        self.assertFalse(INavigationRoot.providedBy(self.folder))
        self.assertTrue(view.available)
        self.assertFalse(view.enabled)

        subsite_view = getMultiAdapter(
            (self.folder, self.request), name="subsite_settings"
        )
        subsite_view.enable()
        self.assertFalse(view.available)

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
