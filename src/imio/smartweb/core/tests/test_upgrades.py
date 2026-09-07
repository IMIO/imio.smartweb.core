# -*- coding: utf-8 -*-

from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.upgrades.upgrades import add_campaignview_to_displayed_types
from imio.smartweb.core.upgrades.upgrades import migrate_section_default_width
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID


class TestUpgrades(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def _set_displayed_types_without_campaignview(self):
        displayed_types = api.portal.get_registry_record("plone.displayed_types")
        api.portal.set_registry_record(
            "plone.displayed_types",
            tuple(t for t in displayed_types if t != "imio.smartweb.CampaignView"),
        )

    def test_add_campaignview_to_displayed_types(self):
        self._set_displayed_types_without_campaignview()
        add_campaignview_to_displayed_types(self.portal)
        self.assertIn(
            "imio.smartweb.CampaignView",
            api.portal.get_registry_record("plone.displayed_types"),
        )

    def test_add_campaignview_to_displayed_types_is_idempotent(self):
        add_campaignview_to_displayed_types(self.portal)
        displayed_types = api.portal.get_registry_record("plone.displayed_types")
        self.assertEqual(
            [t for t in displayed_types if t == "imio.smartweb.CampaignView"],
            ["imio.smartweb.CampaignView"],
        )

    def test_add_campaignview_to_displayed_types_without_ideabox(self):
        self._set_displayed_types_without_campaignview()
        portal_types = api.portal.get_tool("portal_types")
        portal_types.manage_delObjects(["imio.smartweb.CampaignView"])
        add_campaignview_to_displayed_types(self.portal)
        self.assertNotIn(
            "imio.smartweb.CampaignView",
            api.portal.get_registry_record("plone.displayed_types"),
        )

    def test_migrate_section_default_width(self):
        page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            id="page",
        )
        section = api.content.create(
            container=page,
            type="imio.smartweb.SectionText",
            title="Section text",
        )
        section.bootstrap_css_class = None
        migrate_section_default_width(self.portal)
        self.assertEqual(section.bootstrap_css_class, "col-sm-12")

    def test_migrate_section_default_width_is_idempotent(self):
        page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            id="page",
        )
        section = api.content.create(
            container=page,
            type="imio.smartweb.SectionText",
            title="Section text",
        )
        section.bootstrap_css_class = "col-sm-6"
        migrate_section_default_width(self.portal)
        self.assertEqual(section.bootstrap_css_class, "col-sm-6")
