# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from imio.smartweb.core.contents import IDefaultPages
from imio.smartweb.core.contents.folder.views import ElementView
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.app.testing import logout
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import setRoles
from plone.app.z3cform.interfaces import IPloneFormLayer
from plone.testing.zope import Browser
from plone.uuid.interfaces import IUUID
from zope.component import getMultiAdapter
from zope.interface import alsoProvides
from zope.publisher.browser import TestRequest
import transaction


class PagesIntegrationTest(ImioSmartwebTestCase):

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
        self.defaultpage = api.content.create(
            container=self.folder,
            type="imio.smartweb.Page",
            title="Default Page",
            id="defaultpage",
        )
        uuid = IUUID(self.defaultpage)
        self.folder.setLayout("element_view")
        request = TestRequest(
            form={"form.widgets.default_page_uid": uuid, "form.buttons.apply": "Apply"}
        )
        alsoProvides(request, IPloneFormLayer)
        form = ElementView(self.folder, request)
        form.update()

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
        self.assertTrue(page1.exclude_from_nav)
        self.assertTrue(IDefaultPages.providedBy(page1))
        self.assertFalse(page2.exclude_from_nav)
        self.assertFalse(IDefaultPages.providedBy(page2))

        request = TestRequest(
            form={"form.widgets.default_page_uid": uuid2, "form.buttons.apply": "Apply"}
        )
        alsoProvides(request, IPloneFormLayer)
        form = ElementView(self.folder, request)
        form.update()
        data, errors = form.extractData()
        self.assertTrue(len(errors) == 0)
        self.assertTrue(page2.exclude_from_nav)
        self.assertTrue(IDefaultPages.providedBy(page2))
        self.assertFalse(page1.exclude_from_nav)
        self.assertFalse(IDefaultPages.providedBy(page1))

        self.folder.setLayout("block_view")
        self.assertIsNone(self.folder.default_page_uid)
        self.assertFalse(page1.exclude_from_nav)
        self.assertFalse(IDefaultPages.providedBy(page1))
        self.assertFalse(page2.exclude_from_nav)
        self.assertFalse(IDefaultPages.providedBy(page2))

    def test_exclude_from_nav_field(self):
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
        browser.open("{}/edit".format(self.defaultpage.absolute_url()))
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

        page2 = api.content.create(
            container=self.folder, type="imio.smartweb.Page", title="Page 2", id="page2"
        )
        uuid2 = IUUID(page2)
        request = TestRequest(
            form={"form.widgets.default_page_uid": uuid2, "form.buttons.apply": "Apply"}
        )
        alsoProvides(request, IPloneFormLayer)
        form = ElementView(self.folder, request)
        form.update()
        data, errors = form.extractData()
        transaction.commit()

        browser.open("{}/edit".format(self.defaultpage.absolute_url()))
        content = browser.contents
        soup = BeautifulSoup(content)
        exclude_from_nav_widget = soup.find(
            id="form-widgets-IExcludeFromNavigation-exclude_from_nav"
        )
        self.assertIsNotNone(exclude_from_nav_widget.find("input"))

    def test_breadcrumbs(self):
        page1 = api.content.create(
            container=self.folder, type="imio.smartweb.Page", title="Page 1", id="page1"
        )
        self.folder.setLayout("element_view")

        breadcrumbs_view = getMultiAdapter(
            (page1, self.request), name="breadcrumbs_view"
        )
        breadcrumbs = breadcrumbs_view.breadcrumbs()
        self.assertEqual(len(breadcrumbs), 2)
        self.assertEqual(breadcrumbs[-1]["Title"], "Page 1")

        self.folder.set_default_item(
            old_default_item=self.defaultpage, new_default_item=page1
        )
        breadcrumbs_view = getMultiAdapter(
            (page1, self.request), name="breadcrumbs_view"
        )
        breadcrumbs = breadcrumbs_view.breadcrumbs()
        self.assertEqual(len(breadcrumbs), 2)
        self.assertEqual(breadcrumbs[-1]["Title"], "Page 1")

        # Anonymus users should not see default pages in breadcrumbs
        logout()
        breadcrumbs_view = getMultiAdapter(
            (page1, self.request), name="breadcrumbs_view"
        )
        breadcrumbs = breadcrumbs_view.breadcrumbs()
        self.assertEqual(len(breadcrumbs), 1)
        self.assertEqual(breadcrumbs[-1]["Title"], "Folder")

    def test_default_page_removal(self):
        self.assertTrue(self.defaultpage.exclude_from_nav)
        self.assertTrue(IDefaultPages.providedBy(self.defaultpage))
        api.content.delete(self.defaultpage)
        self.assertIsNone(self.folder.default_page_uid)

    def test_default_page_rename(self):
        api.content.rename(obj=self.defaultpage, new_id="foo")
        self.assertTrue(self.defaultpage.exclude_from_nav)
        self.assertTrue(IDefaultPages.providedBy(self.defaultpage))
        self.assertEqual(self.folder.default_page_uid, IUUID(self.defaultpage))

    def test_default_page_cut_and_paste_in_a_folder(self):
        folder2 = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            title="Folder2",
            id="folder2",
        )
        api.content.move(source=self.defaultpage, target=folder2)
        self.assertFalse(self.defaultpage.exclude_from_nav)
        self.assertFalse(IDefaultPages.providedBy(self.defaultpage))
        self.assertIsNone(self.folder.default_page_uid)

    def test_default_page_cut_and_paste_anywhere(self):
        api.content.move(source=self.defaultpage, target=self.portal)
        self.assertFalse(self.defaultpage.exclude_from_nav)
        self.assertFalse(IDefaultPages.providedBy(self.defaultpage))
        self.assertIsNone(self.folder.default_page_uid)

    def test_default_page_copy_and_paste(self):
        copied_page = api.content.copy(source=self.defaultpage, target=self.folder)
        self.assertTrue(self.defaultpage.exclude_from_nav)
        self.assertTrue(IDefaultPages.providedBy(self.defaultpage))
        self.assertEqual(self.folder.default_page_uid, IUUID(self.defaultpage))
        self.assertFalse(copied_page.exclude_from_nav)
        self.assertFalse(IDefaultPages.providedBy(copied_page))

        folder2 = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            title="Folder2",
            id="folder2",
        )
        copied_page = api.content.copy(source=self.defaultpage, target=folder2)
        self.assertTrue(self.defaultpage.exclude_from_nav)
        self.assertTrue(IDefaultPages.providedBy(self.defaultpage))
        self.assertEqual(self.folder.default_page_uid, IUUID(self.defaultpage))
        self.assertFalse(copied_page.exclude_from_nav)
        self.assertFalse(IDefaultPages.providedBy(copied_page))
