# -*- coding: utf-8 -*-

from imio.smartweb.core.contents import IFolder
from imio.smartweb.core.interfaces import IImioSmartwebCoreLayer
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import make_named_image
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import setRoles
from plone.app.textfield.value import RichTextValue
from plone.uuid.interfaces import IUUID
from plone.dexterity.interfaces import IDexterityFTI
from plone.namedfile.file import NamedBlobImage
from plone.testing.zope import Browser
from time import sleep
from zope.annotation.interfaces import IAnnotations
from zope.component import createObject
from zope.component import getMultiAdapter
from zope.component import queryUtility
from zope.interface import alsoProvides
from zope.lifecycleevent import modified

import json
import transaction


class TestFolder(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.authorized_types_in_folder = [
            "Collection",
            "Link",
            "imio.smartweb.Folder",
            "imio.smartweb.Page",
            "imio.smartweb.PortalPage",
            "imio.smartweb.Procedure",
        ]

        self.unauthorized_types_in_folder = ["File", "Image", "Document"]

        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

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
            "IFolder not provided by {0}!".format(
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
            "IFolder not provided by {0}!".format(
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
        self.assertTrue(fti.global_allow, "{0} is not globally addable!".format(fti.id))

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
        for t in self.unauthorized_types_in_folder:
            with self.assertRaises(InvalidParameterError):
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
        page.image = NamedBlobImage(**make_named_image())
        alsoProvides(self.request, IImioSmartwebCoreLayer)
        view = getMultiAdapter((folder, self.request), name="block_view")
        self.assertNotIn("newsImage", view())

        view = getMultiAdapter((folder, self.request), name="block_view_with_images")
        self.assertIn("newsImage", view())
        self.assertEqual(view.get_thumb_scale_summary(), "paysage_vignette")

        self.assertIn("display-paysage", view())
        folder.orientation = "portrait"
        self.assertIn("display-portrait", view())

        api.portal.set_registry_record("plone.thumb_scale_summary", "preview")
        annotations = IAnnotations(self.request)
        del annotations["plone.memoize"]
        view = getMultiAdapter((folder, self.request), name="block_view_with_images")
        self.assertEqual(view.get_thumb_scale_summary(), "preview")

        api.portal.set_registry_record("plone.no_thumbs_summary", True)
        annotations = IAnnotations(self.request)
        del annotations["plone.memoize"]
        view = getMultiAdapter((folder, self.request), name="block_view_with_images")
        self.assertIsNone(view.get_thumb_scale_summary())

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
        self.assertEqual(content.count("<h2"), 2)

        # Anonymous - default page is set on element view
        folder.set_default_item(old_default_item=None, new_default_item=page1)
        transaction.commit()
        browser.open(folder.absolute_url())
        content = browser.contents
        self.assertIn("template-full_view", content)
        self.assertNotIn("template-summary_view", content)
        self.assertIn("<h1>Page 1</h1>", content)

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
            '<h1 class="documentFirstHeading">Form to choose item to be displayed as the home page of the folder</h1>',
            content,
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

    def test_default_page_in_folder_contents(self):
        folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            id="folder",
        )
        page1 = api.content.create(
            container=folder, type="imio.smartweb.Page", id="page1"
        )
        context_info_view = getMultiAdapter(
            (folder, self.request), name="fc-contextInfo"
        )
        result = json.loads(context_info_view())
        self.assertIsNone(result["defaultPage"])

        folder.setLayout("element_view")
        folder.set_default_item(new_default_item=page1)

        result = json.loads(context_info_view())
        self.assertEqual(result["defaultPage"], "page1")

    def test_modification_date(self):
        folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            id="folder",
        )
        first_modification = folder.ModificationDate()
        sleep(1)
        page = api.content.create(
            container=folder,
            type="imio.smartweb.Page",
            title="Page",
        )
        next_modification = folder.ModificationDate()
        self.assertNotEqual(first_modification, next_modification)

        first_modification = folder.ModificationDate()
        sleep(1)
        page.title = "New Page"
        modified(page)
        page.reindexObject()
        next_modification = folder.ModificationDate()
        self.assertNotEqual(first_modification, next_modification)

        first_modification = folder.ModificationDate()
        sleep(1)
        section = api.content.create(
            container=page,
            type="imio.smartweb.SectionText",
            title="Section text",
        )
        modified(section)
        next_modification = folder.ModificationDate()
        self.assertNotEqual(first_modification, next_modification)

        section = api.content.create(
            container=page,
            type="imio.smartweb.SectionGallery",
            title="Section Gallery",
        )
        first_modification = folder.ModificationDate()
        sleep(1)
        api.content.create(
            container=section,
            type="Image",
            title="Image",
        )
        next_modification = folder.ModificationDate()
        self.assertEqual(first_modification, next_modification)

    def test_remove_folder_and_children(self):
        folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            id="folder",
        )
        subfolder = api.content.create(
            container=folder,
            type="imio.smartweb.Folder",
            id="subfolder",
        )
        page1 = api.content.create(
            container=folder,
            type="imio.smartweb.Page",
            id="page1",
        )
        page2 = api.content.create(
            container=subfolder,
            type="imio.smartweb.Page",
            id="page1",
        )
        section_text = api.content.create(
            container=page1,
            type="imio.smartweb.SectionText",
            id="txt",
        )
        api.content.create(
            container=page2,
            type="imio.smartweb.SectionText",
            id="txt",
        )
        section_text.text = RichTextValue(
            "<p>Textsectionbody</p>", "text/html", "text/html"
        )
        section_text.reindexObject()
        api.content.delete(folder)

        uuid = IUUID(folder)
        brains = api.content.find(UID=uuid)
        self.assertEqual(len(brains), 0)

        uuid = IUUID(subfolder)
        brains = api.content.find(UID=uuid)
        self.assertEqual(len(brains), 0)

        uuid = IUUID(page1)
        brains = api.content.find(UID=uuid)
        self.assertEqual(len(brains), 0)

        uuid = IUUID(page2)
        brains = api.content.find(UID=uuid)
        self.assertEqual(len(brains), 0)

    def test_select_view_template(self):
        folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            title="My folder",
        )
        self.request.form = {
            "templateId": "block_view_with_images",
            "form.buttons.apply": "Apply",
        }
        creation_date = folder.ModificationDate()
        view = getMultiAdapter((folder, self.request), name="selectViewTemplate")
        sleep(1)
        view.selectViewTemplate()
        new_date = folder.ModificationDate()
        self.assertNotEqual(creation_date, new_date)
