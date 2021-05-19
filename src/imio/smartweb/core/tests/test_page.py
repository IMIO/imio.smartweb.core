# -*- coding: utf-8 -*-

from imio.smartweb.core.contents import IPage
from imio.smartweb.core.interfaces import IImioSmartwebCoreLayer
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import getMultiAdapter
from zope.component import queryUtility
from zope.interface import alsoProvides


class PageIntegrationTest(ImioSmartwebTestCase):

    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests"""
        self.authorized_types_in_page = [
            "imio.smartweb.SectionContact",
            "imio.smartweb.SectionFiles",
            "imio.smartweb.SectionGallery",
            "imio.smartweb.SectionLinks",
            "imio.smartweb.SectionText",
            "imio.smartweb.SectionVideo",
        ]
        self.unauthorized_types_in_page = ["Document", "Link", "File", "Image"]

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
            u"IPage not provided by {0}!".format(
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
            u"IPage not provided by {0}!".format(
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
        self.assertTrue(
            fti.global_allow, u"{0} is not globally addable!".format(fti.id)
        )

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
        self.assertListEqual(bundles, ["spotlightjs", "flexbin"])
