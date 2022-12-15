# -*- coding: utf-8 -*-

from collective.geolocationbehavior.geolocation import IGeolocatable
from imio.smartweb.core.contents import IPage
from imio.smartweb.core.interfaces import IImioSmartwebCoreLayer
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from plone.formwidget.geolocation.geolocation import Geolocation
from plone.uuid.interfaces import IUUID
from time import sleep
from unittest.mock import patch
from zope.component import createObject
from zope.component import getMultiAdapter
from zope.component import queryUtility
from zope.interface import alsoProvides
from zope.lifecycleevent import modified


class TestPage(ImioSmartwebTestCase):

    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests"""
        self.authorized_types_in_page = [
            "imio.smartweb.SectionContact",
            "imio.smartweb.SectionFiles",
            "imio.smartweb.SectionGallery",
            "imio.smartweb.SectionLinks",
            "imio.smartweb.SectionSelections",
            "imio.smartweb.SectionText",
            "imio.smartweb.SectionVideo",
        ]
        self.unauthorized_types_in_page = [
            "Document",
            "Link",
            "File",
            "Image",
            "imio.smartweb.BlockLink",
            "imio.smartweb.DirectoryView",
            "imio.smartweb.EventsView",
            "imio.smartweb.Folder",
            "imio.smartweb.Footer",
            "imio.smartweb.NewsView",
            "imio.smartweb.Page",
            "imio.smartweb.PortalPage",
            "imio.smartweb.Procedure",
        ]

        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            id="folder",
        )

    def test_ct_page_schema(self):
        fti = queryUtility(IDexterityFTI, name="imio.smartweb.Page")
        schema = fti.lookupSchema()
        self.assertEqual(IPage, schema)

    def test_ct_page_fti(self):
        fti = queryUtility(IDexterityFTI, name="imio.smartweb.Page")
        self.assertTrue(fti)

    def test_ct_page_factory(self):
        fti = queryUtility(IDexterityFTI, name="imio.smartweb.Page")
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IPage.providedBy(obj),
            "IPage not provided by {0}!".format(
                obj,
            ),
        )

    def test_ct_page_adding(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        page = api.content.create(
            container=self.folder,
            type="imio.smartweb.Page",
            title="page",
        )
        self.assertTrue(
            IPage.providedBy(page),
            "IPage not provided by {0}!".format(
                page.id,
            ),
        )
        parent = page.__parent__
        self.assertIn("page", parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=page)
        self.assertNotIn("page", parent.objectIds())

    def test_ct_page_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        fti = queryUtility(IDexterityFTI, name="imio.smartweb.Page")
        self.assertTrue(fti.global_allow, "{0} is not globally addable!".format(fti.id))

    def test_ct_page_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        page = api.content.create(
            container=self.folder,
            type="imio.smartweb.Page",
            title="page",
        )
        for t in self.unauthorized_types_in_page:
            with self.assertRaises(InvalidParameterError):
                api.content.create(
                    container=page,
                    type=t,
                    title="My {}".format(t),
                )
        for t in self.authorized_types_in_page:
            api.content.create(
                container=page,
                type=t,
                title="My {}".format(t),
            )

    def test_js_bundles(self):
        page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="Page",
        )
        alsoProvides(self.request, IImioSmartwebCoreLayer)

        getMultiAdapter((page, self.request), name="full_view")()
        bundles = getattr(self.request, "enabled_bundles", [])
        self.assertEqual(len(bundles), 0)

        api.content.create(
            container=page,
            type="imio.smartweb.SectionGallery",
            title="Gallery",
        )
        getMultiAdapter((page, self.request), name="full_view")()
        bundles = getattr(self.request, "enabled_bundles", [])
        self.assertEqual(len(bundles), 2)
        self.assertListEqual(bundles, ["spotlight", "flexbin"])

    def test_js_bundles_with_contact(self):
        page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="Page",
        )
        alsoProvides(self.request, IImioSmartwebCoreLayer)

        getMultiAdapter((page, self.request), name="full_view")()
        bundles = getattr(self.request, "enabled_bundles", [])
        self.assertEqual(len(bundles), 0)

        section_contact = api.content.create(
            container=page,
            type="imio.smartweb.SectionContact",
            title="Contact",
        )
        getMultiAdapter((page, self.request), name="full_view")()
        bundles = getattr(self.request, "enabled_bundles", [])
        self.assertEqual(len(bundles), 2)
        self.assertListEqual(bundles, ["spotlight", "flexbin"])

        section_contact.gallery_mode = "swiper"
        setattr(self.request, "enabled_bundles", [])
        getMultiAdapter((page, self.request), name="full_view")()
        bundles = getattr(self.request, "enabled_bundles", [])
        self.assertEqual(len(bundles), 1)
        self.assertListEqual(bundles, ["spotlight"])

    def test_modification_date(self):
        page = api.content.create(
            container=self.folder,
            type="imio.smartweb.Page",
            title="Page",
        )
        section = api.content.create(
            container=page,
            type="imio.smartweb.SectionText",
            title="Section text",
        )
        first_modification = page.ModificationDate()
        sleep(1)
        modified(section)
        next_modification = page.ModificationDate()
        self.assertNotEqual(first_modification, next_modification)

        section = api.content.create(
            container=page,
            type="imio.smartweb.SectionGallery",
            title="Section Gallery",
        )
        first_modification = page.ModificationDate()
        sleep(1)
        api.content.create(
            container=section,
            type="Image",
            title="Image",
        )
        next_modification = page.ModificationDate()
        self.assertNotEqual(first_modification, next_modification)

        section = api.content.create(
            container=page,
            type="imio.smartweb.SectionLinks",
            title="Section Links",
        )
        link = api.content.create(
            container=section,
            type="imio.smartweb.BlockLink",
            title="Link 1",
        )
        first_modification = page.ModificationDate()
        sleep(1)
        link.title = "Link 1 - new"
        modified(link)
        next_modification = page.ModificationDate()
        self.assertNotEqual(first_modification, next_modification)

    def test_geolocation(self):
        catalog = api.portal.get_tool("portal_catalog")
        page = api.content.create(
            container=self.folder,
            type="imio.smartweb.Page",
            title="Page",
        )
        uuid = IUUID(page)
        brain = api.content.find(UID=uuid)[0]
        indexes = catalog.getIndexDataForRID(brain.getRID())
        self.assertEqual(indexes.get("latitude"), "")
        self.assertEqual(indexes.get("longitude"), "")

        section = api.content.create(
            container=page,
            type="imio.smartweb.SectionMap",
            title="Section Map",
        )
        brain = api.content.find(UID=uuid)[0]
        indexes = catalog.getIndexDataForRID(brain.getRID())
        self.assertEqual(indexes.get("latitude"), "")
        self.assertEqual(indexes.get("longitude"), "")

        section2 = api.content.create(
            container=page,
            type="imio.smartweb.SectionMap",
            title="Section Map 2",
        )
        IGeolocatable(section2).geolocation = Geolocation(
            latitude="4.5", longitude="45"
        )
        modified(section2)
        brain = api.content.find(UID=uuid)[0]
        indexes = catalog.getIndexDataForRID(brain.getRID())
        self.assertEqual(indexes.get("latitude"), "")
        self.assertEqual(indexes.get("longitude"), "")

        api.content.delete(obj=section)
        brain = api.content.find(UID=uuid)[0]
        indexes = catalog.getIndexDataForRID(brain.getRID())
        self.assertEqual(indexes.get("latitude"), 4.5)
        self.assertEqual(indexes.get("longitude"), 45)

        api.content.delete(obj=section2)
        brain = api.content.find(UID=uuid)[0]
        indexes = catalog.getIndexDataForRID(brain.getRID())
        self.assertEqual(indexes.get("latitude"), "")
        self.assertEqual(indexes.get("longitude"), "")

    def test_section_error(self):
        page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="Page",
        )
        api.content.transition(page, "publish")
        api.content.create(
            container=page,
            type="imio.smartweb.SectionLinks",
            title="Section links",
        )
        view = getMultiAdapter((page, self.request), name="full_view")
        self.assertNotIn("Error in section :", view())
        with patch(
            "imio.smartweb.core.contents.sections.links.view.LinksView.items",
            side_effect=Exception,
        ):
            self.assertIn('Error in section : "Section links"', view())
            logout()
            self.assertNotIn("Error in section :", view())
