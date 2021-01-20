# -*- coding: utf-8 -*-
from imio.smartweb.core.content.page import IPage  # NOQA E501
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
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_page_schema(self):
        fti = queryUtility(IDexterityFTI, name='Page')
        schema = fti.lookupSchema()
        self.assertEqual(IPage, schema)

    def test_ct_page_fti(self):
        fti = queryUtility(IDexterityFTI, name='Page')
        self.assertTrue(fti)

    def test_ct_page_factory(self):
        fti = queryUtility(IDexterityFTI, name='Page')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IPage.providedBy(obj),
            u'IPage not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_page_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='Page',
            id='page',
        )

        self.assertTrue(
            IPage.providedBy(obj),
            u'IPage not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('page', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('page', parent.objectIds())

    def test_ct_page_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Page')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_page_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Page')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'page_id',
            title='Page container',
         )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type='Document',
                title='My Content',
            )
