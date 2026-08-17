# -*- coding: utf-8 -*-

from imio.smartweb.core.browser.controlpanel_siteadmin import (
    ISmartwebSiteAdminControlPanel,
)
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.schema import getFieldNames


class TestControlPanelSiteAdminCookiesConsent(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_new_fields_are_declared(self):
        field_names = getFieldNames(ISmartwebSiteAdminControlPanel)
        self.assertIn("enable_google_analytics", field_names)
        for lang in ("fr", "nl", "de", "en"):
            self.assertIn("analytics_title_{}".format(lang), field_names)
            self.assertIn("analytics_description_{}".format(lang), field_names)

    def test_registry_defaults_after_install(self):
        registry = getUtility(IRegistry)
        self.assertTrue(registry.get("smartweb.enable_google_analytics"))
        for lang in ("fr", "nl", "de", "en"):
            self.assertEqual(
                registry.get("smartweb.analytics_title_{}".format(lang)), u""
            )
            self.assertEqual(
                registry.get("smartweb.analytics_description_{}".format(lang)), u""
            )

    def test_registry_round_trip(self):
        api.portal.set_registry_record("smartweb.enable_google_analytics", False)
        self.assertFalse(
            api.portal.get_registry_record("smartweb.enable_google_analytics")
        )
        api.portal.set_registry_record(
            "smartweb.analytics_title_fr", u"Analyse d'audience"
        )
        self.assertEqual(
            api.portal.get_registry_record("smartweb.analytics_title_fr"),
            u"Analyse d'audience",
        )

    def test_siteadmin_controlpanel_accessible_to_site_administrator(self):
        setRoles(self.portal, TEST_USER_ID, ["Site Administrator"])
        view = self.portal.restrictedTraverse("@@siteadmin-smartweb-controlpanel")
        self.assertIsNotNone(view)
