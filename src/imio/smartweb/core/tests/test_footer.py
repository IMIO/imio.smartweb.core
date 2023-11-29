# -*- coding: utf-8 -*-

from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.viewlets.footer import FooterViewlet
from imio.smartweb.core.viewlets.footer import MinisiteFooterViewlet
from imio.smartweb.core.viewlets.footer import SubsiteFooterViewlet
from imio.smartweb.core.tests.utils import make_named_image
from plone import api
from plone.app.testing import logout
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.namedfile.file import NamedBlobImage
from plone.registry import field
from plone.registry import Record
from plone.registry.interfaces import IRegistry
from unittest.mock import patch
from zope.component import getMultiAdapter
from zope.component import getUtility


class TestFooter(ImioSmartwebTestCase):
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

    def test_add_footer_to_plonesite(self):
        view = getMultiAdapter((self.portal, self.request), name="footer_settings")
        self.assertTrue(view.available())
        viewlet = FooterViewlet(self.portal, self.request, None, None)
        viewlet.update()
        self.assertFalse(viewlet.available())
        view.add_footer()
        footers = self.portal.listFolderContents(
            contentFilter={"portal_type": "imio.smartweb.Footer"}
        )
        self.assertEqual(len(footers), 1)
        self.assertFalse(view.available())
        viewlet = FooterViewlet(self.portal, self.request, None, None)
        viewlet.update()
        self.assertTrue(viewlet.available())
        self.assertEqual(viewlet.footer, footers[0])
        api.content.delete(footers[0])
        self.assertTrue(view.available())

    def test_add_footer_to_folder(self):
        view = getMultiAdapter((self.folder, self.request), name="footer_settings")
        self.assertFalse(view.available())
        view.add_footer()
        footers = self.portal.listFolderContents(
            contentFilter={"portal_type": "imio.smartweb.Footer"}
        )
        self.assertEqual(len(footers), 0)

    def test_add_footer_to_subsite(self):
        footer_view = getMultiAdapter(
            (self.folder, self.request), name="footer_settings"
        )
        self.assertFalse(footer_view.available())
        subsite_view = getMultiAdapter(
            (self.folder, self.request), name="subsite_settings"
        )
        subsite_view.enable()
        self.assertTrue(footer_view.available())
        footer_view.add_footer()
        footers = self.folder.listFolderContents(
            contentFilter={"portal_type": "imio.smartweb.Footer"}
        )
        self.assertEqual(len(footers), 1)
        self.assertFalse(footer_view.available())
        api.content.delete(footers[0])
        self.assertTrue(footer_view.available())

    def test_add_footer_to_nested_subsite(self):
        nested_folder = api.content.create(
            container=self.folder,
            type="imio.smartweb.Folder",
            title="Nested folder",
            id="nested_folder",
        )
        subsite_view = getMultiAdapter(
            (self.folder, self.request), name="subsite_settings"
        )
        subsite_view.enable()
        footer_view = getMultiAdapter(
            (self.folder, self.request), name="footer_settings"
        )
        footer_view.add_footer()

        nested_subsite_view = getMultiAdapter(
            (nested_folder, self.request), name="subsite_settings"
        )
        nested_subsite_view.enable()
        nested_footer_view = getMultiAdapter(
            (nested_folder, self.request), name="footer_settings"
        )
        nested_footer_view.add_footer()

        viewlet = SubsiteFooterViewlet(self.folder, self.request, None, None)
        viewlet.update()
        self.assertTrue(viewlet.available())
        nested_viewlet = SubsiteFooterViewlet(nested_folder, self.request, None, None)
        nested_viewlet.update()
        self.assertTrue(nested_viewlet.available())
        self.assertNotEqual(viewlet.footer, nested_viewlet.footer)

    def test_add_footer_to_minisite(self):
        footer_view = getMultiAdapter(
            (self.folder, self.request), name="footer_settings"
        )
        self.assertFalse(footer_view.available())
        minisite_view = getMultiAdapter(
            (self.folder, self.request), name="minisite_settings"
        )
        minisite_view.enable()
        self.assertTrue(footer_view.available())
        footer_view.add_footer()
        footers = self.folder.listFolderContents(
            contentFilter={"portal_type": "imio.smartweb.Footer"}
        )
        self.assertEqual(len(footers), 1)
        self.assertFalse(footer_view.available())
        api.content.delete(footers[0])
        self.assertTrue(footer_view.available())

    def test_portal_and_minisite_footers(self):
        view = getMultiAdapter((self.portal, self.request), name="footer_settings")
        view.add_footer()
        viewlet = FooterViewlet(self.folder, self.request, None, None)
        viewlet.update()
        self.assertTrue(viewlet.available())
        minisite_view = getMultiAdapter(
            (self.folder, self.request), name="minisite_settings"
        )
        minisite_view.enable()
        viewlet = FooterViewlet(self.folder, self.request, None, None)
        viewlet.update()
        self.assertFalse(viewlet.available())
        footer_view = getMultiAdapter(
            (self.folder, self.request), name="footer_settings"
        )
        footer_view.add_footer()
        viewlet = MinisiteFooterViewlet(self.folder, self.request, None, None)
        viewlet.update()
        self.assertTrue(viewlet.available())

        footer = getattr(self.folder, "footer")
        api.content.create(
            container=footer,
            type="imio.smartweb.SectionText",
            title="Section text",
        )
        viewlet = MinisiteFooterViewlet(self.folder, self.request, None, None)
        viewlet.update()
        sections = viewlet.sections
        self.assertEqual(len(sections), 1)
        self.assertIn("Section text", viewlet.footer())

    def test_exclude_from_parent_listing(self):
        view = getMultiAdapter((self.portal, self.request), name="footer_settings")
        view.add_footer()
        footers = self.portal.listFolderContents(
            contentFilter={"portal_type": "imio.smartweb.Footer"}
        )
        self.assertTrue(footers[0].exclude_from_parent_listing)

    def test_background_style(self):
        footer_view = getMultiAdapter(
            (self.portal, self.request), name="footer_settings"
        )
        footer_view.add_footer()
        footer = getattr(self.portal, "footer")
        viewlet = FooterViewlet(self.portal, self.request, None, None)
        viewlet.update()
        self.assertEqual(viewlet.background_style(), "")
        footer.background_image = NamedBlobImage(**make_named_image())
        self.assertIn(
            "background-image:url(http://nohost/plone/footer/@@images/background_image-750",
            viewlet.background_style(),
        )

    def test_sections_render(self):
        footer_view = getMultiAdapter(
            (self.portal, self.request), name="footer_settings"
        )
        footer_view.add_footer()
        footer = getattr(self.portal, "footer")
        api.content.create(
            container=footer,
            type="imio.smartweb.SectionText",
            title="Section text",
        )
        viewlet = FooterViewlet(self.portal, self.request, None, None)
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
        self.assertIn("Section text", render)
        self.assertNotIn('class="manage-section"', render)
        links_section = api.content.create(
            container=footer,
            type="imio.smartweb.SectionLinks",
            title="Section links",
        )
        api.content.create(
            container=links_section,
            type="imio.smartweb.BlockLink",
            title="My link",
        )
        viewlet.update()
        sections = viewlet.sections
        self.assertEqual(len(sections), 2)
        render = "\n".join(
            [
                getMultiAdapter(
                    (section, self.request), name="full_view_item_without_edit"
                )()
                for section in sections
            ]
        )
        self.assertIn("Section links", render)

    def test_has_gdpr_text(self):
        footer_view = getMultiAdapter(
            (self.portal, self.request), name="footer_settings"
        )
        footer_view.add_footer()
        footer = getattr(self.portal, "footer")
        self.assertEqual(footer.restrictedTraverse("@@has_gdpr_text")(), False)
        registry = getUtility(IRegistry)
        records = registry.records
        record = Record(
            field.Bool(
                title="test",
                required=False,
                description="test",
            )
        )
        records["imio.gdpr.interfaces.IGDPRSettings.is_text_ready"] = record
        api.portal.set_registry_record(
            "imio.gdpr.interfaces.IGDPRSettings.is_text_ready", True
        )
        self.assertEqual(footer.restrictedTraverse("@@has_gdpr_text")(), True)

    def test_section_error(self):
        footer_view = getMultiAdapter(
            (self.portal, self.request), name="footer_settings"
        )
        footer_view.add_footer()
        footer = getattr(self.portal, "footer")
        api.content.create(
            container=footer,
            type="imio.smartweb.SectionLinks",
            title="Section links",
        )
        page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="Page",
        )
        api.content.transition(page, "publish")
        view = getMultiAdapter((page, self.request), name="full_view")
        self.assertNotIn("Error in section :", view())
        with patch(
            "imio.smartweb.core.contents.sections.links.view.LinksView.items",
            side_effect=Exception,
        ):
            self.assertIn('Error in section : "Section links"', view())
            logout()
            self.assertNotIn("Error in section :", view())
