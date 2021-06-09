# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from imio.smartweb.core.behaviors.minisite import IImioSmartwebMinisite
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.viewlets.logo import LogoViewlet
from imio.smartweb.core.viewlets.navigation import GlobalSectionsWithQuickAccessViewlet
from plone import api
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import setRoles
from plone.dexterity.content import ASSIGNABLE_CACHE_KEY
from plone.testing.zope import Browser
from plone.namedfile.file import NamedBlobFile
from z3c.relationfield import RelationValue
from zope.annotation import IAnnotations
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

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

    def test_minisite_navigation(self):
        subfolder = api.content.create(
            container=self.folder,
            type="imio.smartweb.Folder",
            title="Subfolder",
            id="subfolder",
        )
        api.content.create(
            container=subfolder,
            type="imio.smartweb.Page",
            title="Subpage",
            id="subpage",
        )
        view = getMultiAdapter((self.folder, self.request), name="minisite_settings")
        view.enable()
        viewlet = GlobalSectionsWithQuickAccessViewlet(
            self.folder, self.request, None, None
        )
        viewlet.update()
        viewlet.remove_minisites()
        self.assertEqual(len(viewlet.navtree), 2)
        self.assertEqual(len(viewlet.navtree["/plone/folder"]), 2)
        self.assertIn("subfolder", viewlet.render_globalnav())
        self.assertIn("subpage", viewlet.render_globalnav())

    def test_quick_accesses(self):
        api.portal.set_registry_record("plone.navigation_depth", 5)
        view = getMultiAdapter((self.folder, self.request), name="minisite_settings")
        view.enable()
        subfolder = api.content.create(
            container=self.folder,
            type="imio.smartweb.Folder",
            title="Subfolder level 2",
        )
        api.content.create(
            container=subfolder,
            type="imio.smartweb.Folder",
            title="Subfolder level 3 (to display submenu)",
        )
        page = api.content.create(
            container=self.folder,
            type="imio.smartweb.Page",
            title="Quick Page everywhere",
        )
        page_sub = api.content.create(
            container=self.folder,
            type="imio.smartweb.Page",
            title="Quick Page Sub",
        )
        viewlet = GlobalSectionsWithQuickAccessViewlet(
            self.folder, self.request, None, None
        )
        viewlet.update()
        self.assertNotIn('<ul class="quick-access">', viewlet.render_globalnav())

        # Quick access on minisite folder
        intids = getUtility(IIntIds)
        self.folder.quick_access_items = [
            RelationValue(intids.getId(page)),
        ]
        self.folder.reindexObject()
        html = viewlet.render_globalnav()
        self.assertNotIn('<ul class="quick-access">', viewlet.render_globalnav())

        # Quick access on second level folder
        intids = getUtility(IIntIds)
        subfolder.quick_access_items = [
            RelationValue(intids.getId(page)),
            RelationValue(intids.getId(page_sub)),
        ]
        subfolder.reindexObject()
        html = viewlet.render_globalnav()
        self.assertIn('<ul class="quick-access">', viewlet.render_globalnav())

        soup = BeautifulSoup(html)
        qa = soup.find("li", {"class": "subfolder-level-2"}).find(
            "ul", {"class": "quick-access"}
        )

        self.assertEqual(len(qa.find_all("li")), 2)
        self.assertIsNotNone(qa.find("li", {"class": "quick-page-sub"}))

    def test_delete_minisite(self):
        view = getMultiAdapter((self.folder, self.request), name="minisite_settings")
        view.enable()
        api.content.delete(self.folder)

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

    def test_minisite_viewlet_logo(self):
        viewlet = LogoViewlet(self.folder, self.request, None, None)
        viewlet.update()
        self.assertEqual(viewlet.navigation_root_url, "http://nohost/plone")
        html = viewlet.render()
        soup = BeautifulSoup(html)
        img = soup.find("img")
        self.assertEqual(img.get("src"), "http://nohost/plone/logo.png")
        annotations = IAnnotations(self.request)
        del annotations["plone.memoize"]
        view = getMultiAdapter((self.folder, self.request), name="minisite_settings")
        view.enable()
        viewlet = LogoViewlet(self.folder, self.request, None, None)
        viewlet.update()
        self.assertEqual(viewlet.navigation_root_url, "http://nohost/plone/folder")
        self.assertTrue(viewlet.show_title())
        self.assertFalse(viewlet.show_logo())
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
        html = viewlet.render()
        soup = BeautifulSoup(html)
        img = soup.find("img")
        self.assertEqual(
            img.get("src"), "http://nohost/plone/folder/@@images/logo/preview"
        )

        # Title should remain the same on sub-contents
        subfolder = api.content.create(
            container=self.folder,
            type="imio.smartweb.Folder",
            title="Subfolder",
        )
        viewlet = LogoViewlet(subfolder, self.request, None, None)
        viewlet.update()
        self.assertEqual(viewlet.navigation_root_url, "http://nohost/plone/folder")
