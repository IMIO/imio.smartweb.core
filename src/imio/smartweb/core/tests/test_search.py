# -*- coding: utf-8 -*-

from eea.facetednavigation.layout.interfaces import IFacetedLayout
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from zope.component import getMultiAdapter
from zope.component import queryMultiAdapter


class TestFaceted(ImioSmartwebTestCase):

    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    def setUp(self):
        """Custom shared utility setup for tests"""
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_search(self):
        search = queryMultiAdapter((self.portal, self.request), name="search")
        self.assertEqual(search.results().pagesize, 10)
        self.assertEqual(search.results().size, 0)

        search = queryMultiAdapter((self.portal, self.request), name="search")
        self.assertEqual(search.results_news().size, 0)
