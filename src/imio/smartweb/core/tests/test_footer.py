# -*- coding: utf-8 -*-

from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.viewlets.footer import FooterViewlet
from imio.smartweb.core.viewlets.footer import SubsiteFooterViewlet
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.namedfile.file import NamedBlobFile
from plone.registry import field
from plone.registry import Record
from plone.registry.interfaces import IRegistry
from zope.component import getMultiAdapter
from zope.component import getUtility


class FooterIntegrationTest(ImioSmartwebTestCase):

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
        self.assertTrue(view.available)
        viewlet = FooterViewlet(self.portal, self.request, None, None)
        viewlet.update()
        self.assertFalse(viewlet.available())
        view.add_footer()
        footers = self.portal.listFolderContents(
            contentFilter={"portal_type": "imio.smartweb.Footer"}
        )
        self.assertEqual(len(footers), 1)
        self.assertFalse(view.available)
        viewlet = FooterViewlet(self.portal, self.request, None, None)
        viewlet.update()
        self.assertTrue(viewlet.available())
        self.assertEqual(viewlet.footer, footers[0])
        api.content.delete(footers[0])
        self.assertTrue(view.available)

    def test_add_footer_to_folder(self):
        view = getMultiAdapter((self.folder, self.request), name="footer_settings")
        self.assertFalse(view.available)
        view.add_footer()
        footers = self.portal.listFolderContents(
            contentFilter={"portal_type": "imio.smartweb.Footer"}
        )
        self.assertEqual(len(footers), 0)

    def test_add_footer_to_subsite(self):
        footer_view = getMultiAdapter(
            (self.folder, self.request), name="footer_settings"
        )
        self.assertFalse(footer_view.available)
        subsite_view = getMultiAdapter(
            (self.folder, self.request), name="subsite_settings"
        )
        subsite_view.enable()
        self.assertTrue(footer_view.available)
        footer_view.add_footer()
        footers = self.folder.listFolderContents(
            contentFilter={"portal_type": "imio.smartweb.Footer"}
        )
        self.assertEqual(len(footers), 1)
        self.assertFalse(footer_view.available)
        api.content.delete(footers[0])
        self.assertTrue(footer_view.available)

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

    def test_background_style(self):
        footer_view = getMultiAdapter(
            (self.portal, self.request), name="footer_settings"
        )
        footer_view.add_footer()
        footer = getattr(self.portal, "footer")
        viewlet = FooterViewlet(footer, self.request, None, None)
        viewlet.update()
        self.assertEqual(viewlet.background_style(), "")
        footer.background_image = NamedBlobFile(data="file data", filename=u"file.png")
        self.assertIn(
            "background-image:url('http://nohost/plone/footer/@@images/background_image/large')",
            viewlet.background_style(),
        )

    def test_sections_render(self):
        footer_view = getMultiAdapter(
            (self.portal, self.request), name="footer_settings"
        )
        footer_view.add_footer()
        footer = getattr(self.portal, "footer")
        viewlet = FooterViewlet(footer, self.request, None, None)
        viewlet.update()
        api.content.create(
            container=footer,
            type="imio.smartweb.SectionText",
            title="Section text",
        )
        render = "\n".join(viewlet.sections())
        self.assertIn("Section text", render)
        self.assertNotIn('class="manage-section"', render)
        api.content.create(
            container=footer,
            type="imio.smartweb.SectionLinks",
            title="Section links",
        )
        render = "\n".join(viewlet.sections())
        self.assertIn("Section link", render)

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
