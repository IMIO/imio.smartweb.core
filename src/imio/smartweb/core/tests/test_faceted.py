# -*- coding: utf-8 -*-

from eea.facetednavigation.layout.interfaces import IFacetedLayout
from freezegun import freeze_time
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
from zope.component import queryMultiAdapter
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

    @freeze_time("2021-09-14 8:00:00")
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
            '<img src="http://nohost/plone/my-collection/@@images/image/paysage_liste?cache_key=78fd1bab198354b6877aed44e2ea0b4d',
            popup,
        )
        collection.orientation = "portrait"
        popup = popup_view.popup(brain)
        self.assertIn(
            '<img src="http://nohost/plone/my-collection/@@images/image/portrait_liste?cache_key=78fd1bab198354b6877aed44e2ea0b4d',
            popup,
        )

    @freeze_time("2021-09-14 8:00:00")
    def test_get_scale_url(self):
        collection = api.content.create(
            container=self.portal,
            type="Collection",
            title="My collection",
        )
        faceted_view = queryMultiAdapter(
            (collection, self.request), name="faceted-view"
        )

        # page with no lead image
        page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="Page",
        )
        uuid = IUUID(page)
        brain = api.content.find(UID=uuid)[0]
        self.assertEqual(faceted_view.get_scale_url(brain), "")

        # page with lead image
        page.image = NamedBlobImage(**make_named_image())
        page.reindexObject()
        brain = api.content.find(UID=uuid)[0]
        self.assertEqual(
            faceted_view.get_scale_url(brain),
            "http://nohost/plone/page/@@images/image/paysage_vignette?cache_key=78fd1bab198354b6877aed44e2ea0b4d",
        )

        # image orientation
        collection.orientation = "portrait"
        self.assertEqual(
            faceted_view.get_scale_url(brain),
            "http://nohost/plone/page/@@images/image/portrait_vignette?cache_key=78fd1bab198354b6877aed44e2ea0b4d",
        )

        # empty gallery
        gallery = api.content.create(
            container=page,
            type="imio.smartweb.SectionGallery",
            title="Gallery",
        )
        uuid = IUUID(gallery)
        brain = api.content.find(UID=uuid)[0]
        self.assertEqual(faceted_view.get_scale_url(brain), "")

        # gallery with image
        collection.orientation = "paysage"
        image = api.content.create(
            container=gallery,
            type="Image",
            title="Image",
        )
        image.image = NamedBlobImage(**make_named_image())
        brain = api.content.find(UID=uuid)[0]
        faceted_view.get_scale_url(brain)
        scale_url = faceted_view.get_scale_url(brain)
        self.assertNotIn(
            "http://nohost/plone/page/gallery/image/@@images/image/paysage_vignette",
            scale_url,
        )
        self.assertIn(
            "http://nohost/plone/page/gallery/image/@@images/image-430-", scale_url
        )
