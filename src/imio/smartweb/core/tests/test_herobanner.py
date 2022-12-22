# -*- coding: utf-8 -*-

from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.viewlets.herobanner import HeroBannerViewlet
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from zope.component import getMultiAdapter


class TestHeroBanner(ImioSmartwebTestCase):

    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests"""
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            title="Folder",
            id="folder",
        )

    def test_add_herobanner_to_plonesite(self):
        view = getMultiAdapter((self.portal, self.request), name="herobanner_settings")
        self.assertTrue(view.available())
        viewlet = HeroBannerViewlet(self.portal, self.request, None, None)
        viewlet.update()
        self.assertFalse(viewlet.available())
        view.add_herobanner()
        herobanners = self.portal.listFolderContents(
            contentFilter={"portal_type": "imio.smartweb.HeroBanner"}
        )
        self.assertEqual(len(herobanners), 1)
        self.assertFalse(view.available())
        viewlet = HeroBannerViewlet(self.portal, self.request, None, None)
        viewlet.update()
        self.assertTrue(viewlet.available())
        self.assertEqual(viewlet.herobanner, herobanners[0])

        default_page = api.content.create(
            container=self.portal,
            type="imio.smartweb.PortalPage",
            id="portal-page",
        )
        self.portal.setDefaultPage("portal-page")
        viewlet = HeroBannerViewlet(default_page, self.request, None, None)
        viewlet.update()
        self.assertEqual(viewlet.herobanner, herobanners[0])
        view = getMultiAdapter((default_page, self.request), name="herobanner_settings")
        self.assertFalse(view.available())

        api.content.delete(herobanners[0])
        self.assertTrue(view.available())

        view = getMultiAdapter((default_page, self.request), name="herobanner_settings")
        view.add_herobanner()
        herobanners = self.portal.listFolderContents(
            contentFilter={"portal_type": "imio.smartweb.HeroBanner"}
        )
        self.assertEqual(len(herobanners), 1)
        herobanners = default_page.listFolderContents(
            contentFilter={"portal_type": "imio.smartweb.HeroBanner"}
        )
        self.assertEqual(len(herobanners), 0)

    def test_add_herobanner_to_folder(self):
        view = getMultiAdapter((self.folder, self.request), name="herobanner_settings")
        self.assertFalse(view.available())
        view.add_herobanner()
        herobanners = self.portal.listFolderContents(
            contentFilter={"portal_type": "imio.smartweb.HeroBanner"}
        )
        self.assertEqual(len(herobanners), 0)

    def test_add_herobanner_to_minisite(self):
        herobanner_view = getMultiAdapter(
            (self.folder, self.request), name="herobanner_settings"
        )
        self.assertFalse(herobanner_view.available())
        minisite_view = getMultiAdapter(
            (self.folder, self.request), name="minisite_settings"
        )
        minisite_view.enable()
        self.assertTrue(herobanner_view.available())
        herobanner_view.add_herobanner()
        herobanners = self.folder.listFolderContents(
            contentFilter={"portal_type": "imio.smartweb.HeroBanner"}
        )
        self.assertEqual(len(herobanners), 1)
        self.assertFalse(herobanner_view.available())

        default_page = api.content.create(
            container=self.folder,
            type="imio.smartweb.PortalPage",
            id="portal-page",
        )
        self.folder.set_default_item(new_default_item=default_page)
        viewlet = HeroBannerViewlet(default_page, self.request, None, None)
        viewlet.update()
        self.assertEqual(viewlet.herobanner, herobanners[0])
        herobanner_view = getMultiAdapter(
            (default_page, self.request), name="herobanner_settings"
        )
        self.assertFalse(herobanner_view.available())

        api.content.delete(herobanners[0])
        self.assertTrue(herobanner_view.available())

    def test_exclude_from_parent_listing(self):
        view = getMultiAdapter((self.portal, self.request), name="herobanner_settings")
        view.add_herobanner()
        herobanners = self.portal.listFolderContents(
            contentFilter={"portal_type": "imio.smartweb.HeroBanner"}
        )
        self.assertTrue(herobanners[0].exclude_from_parent_listing)

    def test_sections_render(self):
        herobanner_view = getMultiAdapter(
            (self.portal, self.request), name="herobanner_settings"
        )
        herobanner_view.add_herobanner()
        herobanner = getattr(self.portal, "herobanner")
        slide = api.content.create(
            container=herobanner,
            type="imio.smartweb.SectionSlide",
            title="Section slide",
        )
        slide.show_title_and_description = True
        viewlet = HeroBannerViewlet(self.portal, self.request, None, None)
        viewlet.update()
        sections = viewlet.sections
        self.assertEqual(len(sections), 1)
        render = "\n".join(
            [
                getMultiAdapter(
                    (section, self.request), name="full_view_item_without_edit"
                )()
                for section in sections
            ]
        )
        self.assertIn("Section slide", render)
        self.assertNotIn("<h2", render)
        self.assertNotIn('class="manage-section"', render)
        self.assertNotIn("section-container", render)
