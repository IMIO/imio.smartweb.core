# -*- coding: utf-8 -*-

from imio.smartweb.core.contents import IPortalPage
from imio.smartweb.core.interfaces import IImioSmartwebCoreLayer
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.utils import get_default_content_id
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import getMultiAdapter
from zope.component import queryUtility
from zope.interface import alsoProvides


class TestPortalPage(ImioSmartwebTestCase):

    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests"""
        self.authorized_types_in_portal_page = [
            "imio.smartweb.SectionContact",
            "imio.smartweb.SectionFiles",
            "imio.smartweb.SectionGallery",
            "imio.smartweb.SectionLinks",
            "imio.smartweb.SectionSelections",
            "imio.smartweb.SectionText",
            "imio.smartweb.SectionVideo",
        ]
        self.unauthorized_types_in_portal_page = [
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

    def test_ct_portal_page_schema(self):
        fti = queryUtility(IDexterityFTI, name="imio.smartweb.PortalPage")
        schema = fti.lookupSchema()
        self.assertEqual(IPortalPage, schema)

    def test_ct_portal_page_fti(self):
        fti = queryUtility(IDexterityFTI, name="imio.smartweb.PortalPage")
        self.assertTrue(fti)

    def test_ct_portal_page_factory(self):
        fti = queryUtility(IDexterityFTI, name="imio.smartweb.PortalPage")
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IPortalPage.providedBy(obj),
            "IPortalPage not provided by {0}!".format(
                obj,
            ),
        )

    def test_ct_portal_page_adding(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        portal_page = api.content.create(
            container=self.folder,
            type="imio.smartweb.PortalPage",
            title="portal_page",
        )
        self.assertTrue(
            IPortalPage.providedBy(portal_page),
            "IPortalPage not provided by {0}!".format(
                portal_page.id,
            ),
        )
        parent = portal_page.__parent__
        self.assertIn("portal_page", parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=portal_page)
        self.assertNotIn("portal_page", parent.objectIds())

    def test_ct_portal_page_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        fti = queryUtility(IDexterityFTI, name="imio.smartweb.PortalPage")
        self.assertTrue(fti.global_allow, "{0} is not globally addable!".format(fti.id))

    def test_ct_portal_page_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        portal_page = api.content.create(
            container=self.folder,
            type="imio.smartweb.PortalPage",
            title="portal_page",
        )
        for t in self.unauthorized_types_in_portal_page:
            with self.assertRaises(InvalidParameterError):
                api.content.create(
                    container=portal_page,
                    type=t,
                    title="My {}".format(t),
                )
        for t in self.authorized_types_in_portal_page:
            api.content.create(
                container=portal_page,
                type=t,
                title="My {}".format(t),
            )

    def test_js_bundles(self):
        portal_page = api.content.create(
            container=self.portal,
            type="imio.smartweb.PortalPage",
            title="portal_page",
        )
        alsoProvides(self.request, IImioSmartwebCoreLayer)

        getMultiAdapter((portal_page, self.request), name="full_view")()
        bundles = getattr(self.request, "enabled_bundles", [])
        self.assertEqual(len(bundles), 0)

        api.content.create(
            container=portal_page,
            type="imio.smartweb.SectionGallery",
            title="Gallery",
        )
        getMultiAdapter((portal_page, self.request), name="full_view")()
        bundles = getattr(self.request, "enabled_bundles", [])
        self.assertEqual(len(bundles), 2)
        self.assertListEqual(bundles, ["spotlight", "flexbin"])

    def test_js_bundles_with_contact(self):
        portal_page = api.content.create(
            container=self.portal,
            type="imio.smartweb.PortalPage",
            title="portal_page",
        )
        alsoProvides(self.request, IImioSmartwebCoreLayer)

        getMultiAdapter((portal_page, self.request), name="full_view")()
        bundles = getattr(self.request, "enabled_bundles", [])
        self.assertEqual(len(bundles), 0)

        section_contact = api.content.create(
            container=portal_page,
            type="imio.smartweb.SectionContact",
            title="Contact",
        )
        getMultiAdapter((portal_page, self.request), name="full_view")()
        bundles = getattr(self.request, "enabled_bundles", [])
        self.assertEqual(len(bundles), 2)
        self.assertListEqual(bundles, ["spotlight", "flexbin"])

        section_contact.gallery_mode = "swiper"
        setattr(self.request, "enabled_bundles", [])
        getMultiAdapter((portal_page, self.request), name="full_view")()
        bundles = getattr(self.request, "enabled_bundles", [])
        self.assertEqual(len(bundles), 1)
        self.assertListEqual(bundles, ["spotlight"])

    def test_no_title(self):
        portal_page = api.content.create(
            container=self.portal,
            type="imio.smartweb.PortalPage",
            title="My Portal Page",
        )
        view = getMultiAdapter((portal_page, self.request), name="full_view")()
        self.assertNotIn("<h1>", view)

    def test_get_default_content_id(self):
        self.assertEqual(get_default_content_id(self.portal), "")
        api.content.create(
            container=self.portal,
            type="imio.smartweb.PortalPage",
            id="portal-page",
        )
        self.portal.setDefaultPage("portal-page")
        self.assertEqual(get_default_content_id(self.portal), "portal-page")
