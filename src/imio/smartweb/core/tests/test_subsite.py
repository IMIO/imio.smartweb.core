# -*- coding: utf-8 -*-

from imio.smartweb.core.behaviors.subsite import IImioSmartwebSubsite
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.viewlets.subsite import SubsiteLogoViewlet
from imio.smartweb.core.viewlets.subsite import SubsiteNavigationViewlet
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.dexterity.content import ASSIGNABLE_CACHE_KEY
from plone.namedfile.file import NamedBlobFile
from Products.Five.browser import BrowserView as View
from zope.component import getMultiAdapter
from zope.viewlet.interfaces import IViewlet
from zope.viewlet.interfaces import IViewletManager
import unittest


class SubsiteIntegrationTest(unittest.TestCase):

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
        view = getMultiAdapter((self.portal, self.request), name="subsite_settings")
        self.assertFalse(view.available)

        view = getMultiAdapter((self.folder, self.request), name="subsite_settings")
        self.assertTrue(view.available)
        self.assertFalse(view.enabled)

        view.enable()
        self.assertTrue(IImioSmartwebSubsite.providedBy(self.folder))
        self.assertFalse(view.available)
        self.assertTrue(view.enabled)

        view.disable()
        self.assertFalse(IImioSmartwebSubsite.providedBy(self.folder))
        self.assertTrue(view.available)
        self.assertFalse(view.enabled)

    def test_viewlet_navigation(self):
        view = getMultiAdapter((self.folder, self.request), name="subsite_settings")
        view.enable()

        api.content.create(
            container=self.folder, type="imio.smartweb.Page", title="Page 1", id="page1"
        )
        subfolder = api.content.create(
            container=self.folder,
            type="imio.smartweb.Folder",
            title="Subfolder",
            id="subfolder",
        )
        api.content.create(
            container=subfolder,
            type="imio.smartweb.Page",
            title="Sub Page 1",
            id="subpage1",
        )

        viewlet = SubsiteNavigationViewlet(self.portal, self.request, None, None)
        viewlet.update()
        self.assertFalse(viewlet.available())

        viewlet = SubsiteNavigationViewlet(self.folder, self.request, None, None)
        viewlet.update()
        self.assertTrue(viewlet.available())
        self.assertEqual(len(viewlet.portal_tabs), 2)

        viewlet = SubsiteNavigationViewlet(subfolder, self.request, None, None)
        viewlet.update()
        self.assertTrue(viewlet.available())
        self.assertEqual(viewlet.subsite_root, self.folder)
        self.assertEqual(len(viewlet.portal_tabs), 2)
        self.assertEqual(
            viewlet.render_globalnav(),
            '<li class="page1 nav-item"><a href="http://nohost/plone/folder/page1" class="state-private nav-link">Page 1</a></li><li class="subfolder nav-item"><a href="http://nohost/plone/folder/subfolder" class="state-private nav-link">Subfolder</a></li>',
        )
        self.assertNotIn("Sub Page 1", viewlet.render_globalnav())

        self.folder.menu_depth = 2
        viewlet = SubsiteNavigationViewlet(self.folder, self.request, None, None)
        viewlet.update()
        self.assertIn("Sub Page 1", viewlet.render_globalnav())

    def test_viewlet_logo(self):
        view = getMultiAdapter((self.folder, self.request), name="subsite_settings")
        view.enable()
        viewlet = SubsiteLogoViewlet(self.folder, self.request, None, None)
        viewlet.update()
        self.assertTrue(viewlet.available())
        self.assertTrue(viewlet.show_title())
        self.assertFalse(viewlet.show_logo())

        view = View(self.folder, self.request)
        manager = getMultiAdapter(
            (self.folder, self.request, view),
            IViewletManager,
            name="plone.portalheader",
        )
        viewlet = getMultiAdapter(
            (self.folder, self.request, view, manager),
            IViewlet,
            name="imio.smartweb.subsite_logo",
        )
        self.assertIn("Folder", viewlet())
        self.folder.logo_display_mode = "logo"
        self.assertFalse(viewlet.show_title())
        self.assertFalse(viewlet.show_logo())
        self.folder.logo_display_mode = "logo_title"
        self.assertTrue(viewlet.show_title())
        self.assertFalse(viewlet.show_logo())
        self.folder.logo = NamedBlobFile(data="file data", filename=u"file.png")
        self.assertTrue(viewlet.show_logo())
        self.folder.logo_display_mode = "logo"
        self.assertTrue(viewlet.show_logo())

        # Title should remain the same on sub-contents
        subfolder = api.content.create(
            container=self.folder,
            type="imio.smartweb.Folder",
            title="Subfolder",
        )
        view = View(subfolder, self.request)
        manager = getMultiAdapter(
            (subfolder, self.request, view), IViewletManager, name="plone.portalheader"
        )
        viewlet = getMultiAdapter(
            (subfolder, self.request, view, manager),
            IViewlet,
            name="imio.smartweb.subsite_logo",
        )
        self.assertIn("Folder", viewlet())
        self.assertNotIn("Subfolder", viewlet())
