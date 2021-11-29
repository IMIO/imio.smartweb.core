# -*- coding: utf-8 -*-

from eea.facetednavigation.layout.interfaces import IFacetedLayout
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from zope.component import getMultiAdapter


class TestFaceted(ImioSmartwebTestCase):

    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    def setUp(self):
        """Custom shared utility setup for tests"""
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.collection = api.content.create(
            container=self.portal,
            type="Collection",
            title="A collection",
            id="a-collection",
        )

    def test_faceted_body_class(self):
        template = self.collection.restrictedTraverse("view")
        view = getMultiAdapter((self.collection, self.request), name="view")
        layout_view = self.collection.restrictedTraverse("@@plone_layout")
        body_class = layout_view.bodyClass(template, view)
        self.assertIn("faceted-block-view", body_class)

        IFacetedLayout(self.collection).update_layout(
            "faceted-summary-view-with-images"
        )
        body_class = layout_view.bodyClass(template, view)
        self.assertIn("faceted-summary-view-with-images", body_class)

        subtyper = self.collection.restrictedTraverse("@@faceted_subtyper")
        subtyper.disable()
        view = getMultiAdapter((self.collection, self.request), name="view")
        body_class = layout_view.bodyClass(template, view)
        self.assertNotIn("faceted-summary-view-with-images", body_class)
