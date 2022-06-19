# -*- coding: utf-8 -*-

from eea.facetednavigation.layout.interfaces import IFacetedLayout
from imio.smartweb.core.interfaces import IImioSmartwebCoreLayer
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import make_named_image
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.namedfile.file import NamedBlobImage
from plone.uuid.interfaces import IUUID
from zope.component import getMultiAdapter
from zope.interface import alsoProvides


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

        IFacetedLayout(self.collection).update_layout("faceted-map")
        body_class = layout_view.bodyClass(template, view)
        self.assertIn("faceted-map", body_class)

        subtyper = self.collection.restrictedTraverse("@@faceted_subtyper")
        subtyper.disable()
        view = getMultiAdapter((self.collection, self.request), name="view")
        body_class = layout_view.bodyClass(template, view)
        self.assertNotIn("faceted-summary-view-with-images", body_class)

    def test_map_popup(self):
        alsoProvides(self.request, IImioSmartwebCoreLayer)
        collection = api.content.create(
            container=self.portal,
            type="Collection",
            title="My collection",
            description="My **description**",
        )
        uuid = IUUID(collection)
        brain = api.content.find(UID=uuid)[0]
        popup_view = getMultiAdapter(
            (collection, self.request), name="faceted-map-geojson-popup"
        )
        popup = popup_view.popup(brain)
        self.assertNotIn("<img", popup)
        self.assertIn('href="http://nohost/plone/my-collection"', popup)
        self.assertIn("My collection", popup)
        self.assertIn("My description", popup)

        collection.image = NamedBlobImage(**make_named_image())
        collection.reindexObject()
        brain = api.content.find(UID=uuid)[0]
        popup = popup_view.popup(brain)
        self.assertIn(
            '<img src="http://nohost/plone/my-collection/@@images/image/mini"', popup
        )
