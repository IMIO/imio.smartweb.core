# -*- coding: utf-8 -*-

from imio.smartweb.core.contents import IDefaultPages
from imio.smartweb.core.contents.folder.views import ElementView
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.app.z3cform.interfaces import IPloneFormLayer
from plone.uuid.interfaces import IUUID
from zope.component import getMultiAdapter
from zope.interface import alsoProvides
from zope.publisher.browser import TestRequest
import unittest


class PagesIntegrationTest(unittest.TestCase):

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

    def test_no_change(self):
        api.content.create(
            container=self.folder, type="imio.smartweb.Page", title="Page 1", id="page1"
        )
        self.folder.setLayout("element_view")
        request = TestRequest(form={"form.buttons.apply": "Apply"})
        alsoProvides(request, IPloneFormLayer)
        form = ElementView(self.folder, request)
        form.update()
        data, errors = form.extractData()
        self.assertTrue(len(errors) == 0)
        self.assertEqual(form.status, "No changes were applied.")

    def test_exclude_from_nav(self):
        page1 = api.content.create(
            container=self.folder, type="imio.smartweb.Page", title="Page 1", id="page1"
        )
        page2 = api.content.create(
            container=self.folder, type="imio.smartweb.Page", title="Page 2", id="page2"
        )
        uuid1 = IUUID(page1)
        uuid2 = IUUID(page2)
        self.folder.setLayout("element_view")
        request = TestRequest(
            form={"form.widgets.default_page_uid": uuid1, "form.buttons.apply": "Apply"}
        )
        alsoProvides(request, IPloneFormLayer)
        form = ElementView(self.folder, request)
        form.update()
        data, errors = form.extractData()
        self.assertTrue(len(errors) == 0)
        self.assertEqual(page1.exclude_from_nav, True)
        self.assertEqual(IDefaultPages.providedBy(page1), True)
        self.assertEqual(page2.exclude_from_nav, False)
        self.assertEqual(IDefaultPages.providedBy(page2), False)

        request = TestRequest(
            form={"form.widgets.default_page_uid": uuid2, "form.buttons.apply": "Apply"}
        )
        alsoProvides(request, IPloneFormLayer)
        form = ElementView(self.folder, request)
        form.update()
        data, errors = form.extractData()
        self.assertTrue(len(errors) == 0)
        self.assertEqual(page2.exclude_from_nav, True)
        self.assertEqual(IDefaultPages.providedBy(page2), True)
        self.assertEqual(page1.exclude_from_nav, False)
        self.assertEqual(IDefaultPages.providedBy(page1), False)

        self.folder.setLayout("block_view")
        self.assertIsNone(self.folder.default_page_uid)
        self.assertEqual(page1.exclude_from_nav, False)
        self.assertEqual(IDefaultPages.providedBy(page1), False)
        self.assertEqual(page2.exclude_from_nav, False)
        self.assertEqual(IDefaultPages.providedBy(page2), False)

    def test_breadcrumbs(self):
        page1 = api.content.create(
            container=self.folder, type="imio.smartweb.Page", title="Page 1", id="page1"
        )
        uuid1 = IUUID(page1)
        self.folder.setLayout("element_view")

        breadcrumbs_view = getMultiAdapter(
            (page1, self.request), name="breadcrumbs_view"
        )
        breadcrumbs = breadcrumbs_view.breadcrumbs()
        self.assertEqual(len(breadcrumbs), 2)
        self.assertEqual(breadcrumbs[-1]["Title"], "Page 1")

        request = TestRequest(
            form={"form.widgets.default_page_uid": uuid1, "form.buttons.apply": "Apply"}
        )
        alsoProvides(request, IPloneFormLayer)
        form = ElementView(self.folder, request)
        form.update()
        data, errors = form.extractData()
        breadcrumbs_view = getMultiAdapter(
            (page1, self.request), name="breadcrumbs_view"
        )
        breadcrumbs = breadcrumbs_view.breadcrumbs()
        self.assertEqual(len(breadcrumbs), 1)
        self.assertEqual(breadcrumbs[-1]["Title"], "Folder")

    def test_default_page_removal(self):
        page1 = api.content.create(
            container=self.folder, type="imio.smartweb.Page", title="Page 1", id="page1"
        )
        uuid1 = IUUID(page1)
        self.folder.setLayout("element_view")
        request = TestRequest(
            form={"form.widgets.default_page_uid": uuid1, "form.buttons.apply": "Apply"}
        )
        alsoProvides(request, IPloneFormLayer)
        form = ElementView(self.folder, request)
        form.update()
        data, errors = form.extractData()
        self.assertTrue(len(errors) == 0)
        self.assertEqual(page1.exclude_from_nav, True)
        self.assertEqual(IDefaultPages.providedBy(page1), True)

        api.content.delete(page1)
        self.assertIsNone(self.folder.default_page_uid)
