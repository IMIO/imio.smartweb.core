# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.folder.content import IFolder
from imio.smartweb.core.contents.folder.views import ElementView
from imio.smartweb.core.interfaces import IImioSmartwebCoreLayer
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.tests.utils import get_leadimage_filename
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import setRoles
from plone.app.z3cform.interfaces import IPloneFormLayer
from plone.uuid.interfaces import IUUID
from plone.dexterity.interfaces import IDexterityFTI
from plone.namedfile.file import NamedBlobFile
from plone.testing.z2 import Browser
from zope.component import createObject
from zope.component import getMultiAdapter
from zope.component import queryUtility
from zope.interface import alsoProvides
from zope.publisher.browser import TestRequest
import unittest
import transaction


class FolderFunctionalTest(unittest.TestCase):

    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.authorized_types_in_folder = [
            "Collection",
            "Link",
            "imio.smartweb.Folder",
            "imio.smartweb.Page",
            "imio.smartweb.Procedure",
        ]

        self.unauthorized_types_in_folder = ["File", "Image", "Document"]

        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.parent = self.portal

    def test_ct_folder_schema(self):
        fti = queryUtility(IDexterityFTI, name="imio.smartweb.Folder")
        schema = fti.lookupSchema()
        self.assertEqual(IFolder, schema)

    def test_ct_folder_fti(self):
        fti = queryUtility(IDexterityFTI, name="imio.smartweb.Folder")
        self.assertTrue(fti)

    def test_ct_folder_factory(self):
        fti = queryUtility(IDexterityFTI, name="imio.smartweb.Folder")
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IFolder.providedBy(obj),
            u"IFolder not provided by {0}!".format(
                obj,
            ),
        )

    def test_ct_folder_adding(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        obj = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            id="folder",
        )

        self.assertTrue(
            IFolder.providedBy(obj),
            u"IFolder not provided by {0}!".format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn("folder", parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn("folder", parent.objectIds())

    def test_ct_folder_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        fti = queryUtility(IDexterityFTI, name="imio.smartweb.Folder")
        self.assertTrue(
            fti.global_allow, u"{0} is not globally addable!".format(fti.id)
        )

    def test_ct_folder_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        fti = queryUtility(IDexterityFTI, name="imio.smartweb.Folder")
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            "folder_id",
            title="Folder container",
        )
        folder = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            for t in self.unauthorized_types_in_folder:
                api.content.create(
                    container=folder,
                    type=t,
                    title="My {}".format(t),
                )
        for t in self.authorized_types_in_folder:
            api.content.create(
                container=folder,
                type=t,
                title="My {}".format(t),
            )

    def test_leadimage_in_folder_block_view(self):
        folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            title="My folder",
        )
        page = api.content.create(
            container=folder,
            type="imio.smartweb.Page",
            title="My page",
        )
        page.image = NamedBlobFile("ploneLeadImage", filename=get_leadimage_filename())
        alsoProvides(self.request, IImioSmartwebCoreLayer)
        view = getMultiAdapter((folder, self.request), name="block_view")
        self.assertNotIn("newsImage", view())
        view = getMultiAdapter((folder, self.request), name="block_view_with_images")
        self.assertIn("newsImage", view())
        self.assertEqual(view.get_thumb_scale(), "mini")
        api.portal.set_registry_record("plone.thumb_scale_summary", "preview")
        self.assertEqual(view.get_thumb_scale(), "preview")
        api.portal.set_registry_record("plone.no_thumbs_summary", True)
        self.assertIsNone(view.get_thumb_scale())

    def test_element_view_as_anonymous(self):
        folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            title="Folder",
            id="folder",
        )
        api.content.transition(folder, "publish")
        page1 = api.content.create(
            container=folder,
            type="imio.smartweb.Page",
            title="Page 1",
            id="page1",
        )
        api.content.transition(page1, "publish")
        page2 = api.content.create(
            container=folder,
            type="imio.smartweb.Page",
            title="Page 2",
            id="page2",
        )
        api.content.transition(page2, "publish")
        folder.setLayout("element_view")
        transaction.commit()

        # Anonymous - no default page set on element view
        browser = Browser(self.layer["app"])
        browser.open(folder.absolute_url())
        content = browser.contents
        self.assertIn("template-summary_view", content)
        self.assertNotIn("template-full_view", content)
        self.assertEqual(content.count("tileHeadline"), 2)

        # Anonymous - default page is set on element view
        uuid = IUUID(page1)
        request = TestRequest(
            form={"form.widgets.default_page_uid": uuid, "form.buttons.apply": "Apply"}
        )
        alsoProvides(request, IPloneFormLayer)
        form = ElementView(folder, request)
        form.update()
        transaction.commit()
        browser.open(folder.absolute_url())
        content = browser.contents
        self.assertIn("template-full_view", content)
        self.assertNotIn("template-summary_view", content)
        self.assertIn('<h1 class="documentFirstHeading">Page 1</h1>', content)

    def test_element_view_as_editor(self):
        folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            title="Folder",
            id="folder",
        )
        page1 = api.content.create(
            container=folder,
            type="imio.smartweb.Page",
            title="Page 1",
            id="page1",
        )
        uuid = IUUID(page1)
        api.content.create(
            container=folder,
            type="imio.smartweb.Page",
            title="Page 2",
            id="page2",
        )
        folder.setLayout("element_view")
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
        browser.open(folder.absolute_url())
        content = browser.contents
        self.assertIn(
            '<h1 class="documentFirstHeading">Element view form</h1>', content
        )
        radio_control = browser.getControl(name="form.widgets.default_page_uid")
        self.assertIn(uuid, radio_control.options)
        self.assertEqual(radio_control.value, [])
        radio_control.value = uuid
        browser.getControl(name="form.buttons.apply").click()
        content = browser.contents
        self.assertIn("Data successfully updated.", content)
        radio_control = browser.getControl(name="form.widgets.default_page_uid")
        self.assertEqual(radio_control.value, [uuid])
