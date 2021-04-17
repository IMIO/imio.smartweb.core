# -*- coding: utf-8 -*-

from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.viewlets.navigation import GlobalSectionsWithQuickAccessViewlet
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.content import ASSIGNABLE_CACHE_KEY
from zope.component import getMultiAdapter
import unittest


class NavigationFunctionalTest(unittest.TestCase):

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

    def test_quick_accesses(self):
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
        subsubsubfolder = api.content.create(
            container=subsubfolder,
            type="imio.smartweb.Folder",
            title="Subfolder level 4",
        )
        page = api.content.create(
            container=subsubsubfolder,
            type="imio.smartweb.Page",
            title="Quick Page",
        )
        viewlet = GlobalSectionsWithQuickAccessViewlet(
            self.portal, self.request, None, None
        )
        viewlet.update()

        self.assertNotIn("Quick Page", viewlet.render_globalnav())
        self.assertNotIn('<ul class="quick-access">', viewlet.render_globalnav())
        page.include_in_quick_access = True
        page.reindexObject()
        self.assertIn("Quick Page", viewlet.render_globalnav())
        self.assertIn('<ul class="quick-access">', viewlet.render_globalnav())
