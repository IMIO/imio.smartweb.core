# -*- coding: utf-8 -*-
from imio.smartweb.core.contents.page.content import IPage  # NOQA E501
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING  # noqa
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class PageIntegrationTest(unittest.TestCase):

    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.authorized_types_in_page = ["File", "Image"]
        self.unauthorized_types_in_page = ["Document", "Link"]

        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.parent = self.portal
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
        with self.assertRaises(InvalidParameterError):
            for t in self.unauthorized_types_in_page:
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
