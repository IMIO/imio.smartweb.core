# -*- coding: utf-8

from imio.smartweb.core.interfaces import IImioSmartwebCoreLayer
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from plone import api
from plone.app.testing import login
from plone.app.testing import logout
from zope.component import getMultiAdapter
from zope.interface import alsoProvides
import unittest


class ProcedureFunctionalTest(unittest.TestCase):

    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    def _changeUser(self, loginName):
        logout()
        login(self.portal, loginName)
        self.member = api.user.get_current()
        self.request["AUTHENTICATED_USER"] = self.member

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self._changeUser("test")

    def test_quick_access(self):
        page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="Quick access page",
            include_in_quick_access=True,
        )
        brains = api.content.find(include_in_quick_access=True)
        self.assertEqual(len(brains), 1)
        self.assertEqual(page, brains[0].getObject())
        page.include_in_quick_access = False
        page.reindexObject()
        brains = api.content.find(include_in_quick_access=True)
        self.assertEqual(len(brains), 0)

    def test_summary_listing(self):
        folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            title="Folder",
        )
        api.content.create(
            container=folder,
            type="imio.smartweb.Folder",
            title="Sub folder",
            id="subfolder",
        )
        page1 = api.content.create(
            container=folder,
            type="imio.smartweb.Page",
            title="Page 1",
            id="page1",
        )
        api.content.create(
            container=folder,
            type="imio.smartweb.Page",
            title="Page 2",
            id="page2",
        )
        alsoProvides(self.request, IImioSmartwebCoreLayer)
        view = getMultiAdapter((folder, self.request), name="summary_view")
        results = view.results()
        self.assertEqual(len(results), 3)

        # a page can be excluded from parent listing
        page1.exclude_from_parent_listing = True
        page1.reindexObject()
        results = view.results()
        self.assertEqual(len(results), 2)

    def test_block_listing(self):
        folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            title="Folder",
        )
        subfolder = api.content.create(
            container=folder,
            type="imio.smartweb.Folder",
            title="Sub folder",
            id="subfolder",
        )
        page1 = api.content.create(
            container=folder,
            type="imio.smartweb.Page",
            title="Page 1",
            id="page1",
        )
        page2 = api.content.create(
            container=folder,
            type="imio.smartweb.Page",
            title="Page 2",
            id="page2",
        )
        sub_page = api.content.create(
            container=subfolder,
            type="imio.smartweb.Page",
            title="Sub page",
            id="subpage",
        )
        alsoProvides(self.request, IImioSmartwebCoreLayer)
        view = getMultiAdapter((folder, self.request), name="block_view")
        results = view.blocks_results()
        self.assertEqual(len(results["results"]), 3)
        self.assertEqual(len(results["quick_access"]), 0)

        # a sub page can be included in quick access
        sub_page.include_in_quick_access = True
        sub_page.reindexObject()
        results = view.blocks_results()
        self.assertEqual(len(results["results"]), 3)
        self.assertEqual(len(results["quick_access"]), 1)

        # a page can be excluded from parent listing
        page1.exclude_from_parent_listing = True
        page1.reindexObject()
        results = view.blocks_results()
        self.assertEqual(len(results["results"]), 2)
        self.assertEqual(len(results["quick_access"]), 1)

        # an excluded page can still be included in quick access
        page1.include_in_quick_access = True
        page1.reindexObject()
        results = view.blocks_results()
        self.assertEqual(len(results["results"]), 2)
        self.assertEqual(len(results["quick_access"]), 2)

        results_ids = [b.id for b in results["results"]]
        quick_access_ids = [b.id for b in results["quick_access"]]
        self.assertListEqual(results_ids, ["subfolder", "page2"])
        self.assertListEqual(quick_access_ids, ["page1", "subpage"])

        # the same page cannot be included in quick access and in parent listing
        page2.include_in_quick_access = True
        page2.reindexObject()
        results = view.blocks_results()
        self.assertEqual(len(results["results"]), 2)
        self.assertEqual(len(results["quick_access"]), 2)
        results_ids = [b.id for b in results["results"]]
        quick_access_ids = [b.id for b in results["quick_access"]]
        self.assertIn("page2", results_ids)
        self.assertNotIn("page2", quick_access_ids)
