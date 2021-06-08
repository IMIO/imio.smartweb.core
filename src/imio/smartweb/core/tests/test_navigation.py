# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.viewlets.navigation import GlobalSectionsWithQuickAccessViewlet
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.content import ASSIGNABLE_CACHE_KEY
from z3c.relationfield import RelationValue
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.intid.interfaces import IIntIds


class NavigationFunctionalTest(ImioSmartwebTestCase):

    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
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

    def test_remove_subsites_children(self):
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
        viewlet = GlobalSectionsWithQuickAccessViewlet(
            self.portal, self.request, None, None
        )
        viewlet.update()
        self.assertEqual(len(viewlet.navtree), 3)
        self.assertEqual(len(viewlet.navtree["/plone/folder"]), 1)
        self.assertIn("subfolder", viewlet.render_globalnav())
        self.assertIn("subpage", viewlet.render_globalnav())
        view = getMultiAdapter((self.folder, self.request), name="subsite_settings")
        view.enable()
        viewlet.remove_subsites_children()
        self.assertEqual(len(viewlet.navtree), 1)
        self.assertEqual(len(viewlet.navtree["/plone/folder"]), 0)
        self.assertNotIn("subfolder", viewlet.render_globalnav())
        self.assertNotIn("subpage", viewlet.render_globalnav())

    def test_remove_minisite(self):
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
        viewlet = GlobalSectionsWithQuickAccessViewlet(
            self.portal, self.request, None, None
        )
        viewlet.update()
        self.assertEqual(len(viewlet.navtree), 3)
        self.assertEqual(len(viewlet.navtree["/plone/folder"]), 1)
        self.assertIn("subfolder", viewlet.render_globalnav())
        self.assertIn("subpage", viewlet.render_globalnav())
        view = getMultiAdapter((self.folder, self.request), name="minisite_settings")
        view.enable()
        viewlet.remove_minisites()
        self.assertEqual(len(viewlet.navtree), 1)
        self.assertEqual(len(viewlet.navtree["/plone/folder"]), 0)
        self.assertNotIn("subfolder", viewlet.render_globalnav())
        self.assertNotIn("subpage", viewlet.render_globalnav())

    def test_quick_accesses(self):
        api.portal.set_registry_record("plone.navigation_depth", 4)
        subfolder = api.content.create(
            container=self.folder,
            type="imio.smartweb.Folder",
            title="Subfolder level 2",
        )
        subsubfolder = api.content.create(
            container=subfolder,
            type="imio.smartweb.Folder",
            title="Subfolder level 3",
        )
        api.content.create(
            container=subsubfolder,
            type="imio.smartweb.Folder",
            title="Subfolder level 4 (to display submenu)",
        )
        page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="Quick Page everywhere",
        )
        page_sub = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="Quick Page Sub",
        )
        page_sub_sub = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="Quick Page Su-Sub",
        )
        viewlet = GlobalSectionsWithQuickAccessViewlet(
            self.portal, self.request, None, None
        )
        viewlet.update()
        self.assertNotIn('<ul class="quick-access">', viewlet.render_globalnav())

        # Quick access on first level folder
        intids = getUtility(IIntIds)
        self.folder.quick_access_items = [
            RelationValue(intids.getId(page)),
        ]
        self.folder.reindexObject()
        html = viewlet.render_globalnav()
        self.assertIn('<ul class="quick-access">', html)
        self.assertEqual(html.count('<ul class="quick-access">'), 1)

        soup = BeautifulSoup(html)
        qa = soup.find("li", {"class": "folder"}).find("ul", {"class": "quick-access"})

        self.assertEqual(len(qa.find_all("li")), 1)
        self.assertIsNotNone(qa.find("li", {"class": "quick-page-everywhere"}))

        # Quick access on second level folder
        intids = getUtility(IIntIds)
        subfolder.quick_access_items = [
            RelationValue(intids.getId(page)),
            RelationValue(intids.getId(page_sub)),
        ]
        subfolder.reindexObject()
        html = viewlet.render_globalnav()
        self.assertEqual(html.count('<ul class="quick-access">'), 2)

        soup = BeautifulSoup(html)
        qa = soup.find("li", {"class": "subfolder-level-2"}).find(
            "ul", {"class": "quick-access"}
        )

        self.assertEqual(len(qa.find_all("li")), 2)
        self.assertIsNotNone(qa.find("li", {"class": "quick-page-sub"}))

        # Quick access on third level folder
        intids = getUtility(IIntIds)
        subsubfolder.quick_access_items = [
            RelationValue(intids.getId(page)),
            RelationValue(intids.getId(page_sub_sub)),
        ]
        subsubfolder.reindexObject()
        html = viewlet.render_globalnav()
        self.assertEqual(html.count('<ul class="quick-access">'), 3)

        soup = BeautifulSoup(html)
        qa = soup.find("li", {"class": "subfolder-level-3"}).find(
            "ul", {"class": "quick-access"}
        )

        self.assertEqual(len(qa.find_all("li")), 2)
        self.assertIsNotNone(qa.find("li", {"class": "quick-page-su-sub"}))
