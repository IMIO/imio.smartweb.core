# -*- coding: utf-8 -*-

from plone import api
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.browser.dashboards.plausible import PlausibleView
from unittest import mock
from zope.component import queryMultiAdapter

import os


class Testplausible(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests"""
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]

    def set_registry_records(self):
        api.portal.set_registry_record("smartweb.plausible_site", "site-registry.be")
        api.portal.set_registry_record("smartweb.plausible_token", "token-registry")
        api.portal.set_registry_record("smartweb.plausible_url", "url-registry.be")

    @mock.patch.dict(
        os.environ,
        {
            "SMARTWEB_PLAUSIBLE_SITE": "",
            "SMARTWEB_PLAUSIBLE_TOKEN": "",
            "SMARTWEB_PLAUSIBLE_URL": "",
        },
    )
    def test_noenv(self):
        view = PlausibleView(self.portal, self.request)
        self.assertFalse(view.is_plausible_set)
        self.set_registry_records()
        self.assertTrue(view.is_plausible_set)
        self.assertEqual(
            view.get_iframe_src,
            "https://url-registry.be/share/site-registry.be?auth=token-registry&embed=true&theme=light&background=transparent",
        )
        self.assertEqual(
            view.get_embedhostjs_src,
            "https://url-registry.be/js/embed.host.js",
        )

    @mock.patch.dict(
        os.environ,
        {
            "SMARTWEB_PLAUSIBLE_SITE": "site-varenv.be",
            "SMARTWEB_PLAUSIBLE_TOKEN": "token-varenv",
            "SMARTWEB_PLAUSIBLE_URL": "url-varenv.be",
        },
    )
    def test_env(self):
        view = PlausibleView(self.portal, self.request)
        self.assertTrue(view.is_plausible_set)
        self.assertEqual(
            view.get_iframe_src,
            "https://url-varenv.be/share/site-varenv.be?auth=token-varenv&embed=true&theme=light&background=transparent",
        )
        self.assertEqual(
            view.get_embedhostjs_src,
            "https://url-varenv.be/js/embed.host.js",
        )
        self.set_registry_records()
        self.assertEqual(
            view.get_iframe_src,
            "https://url-varenv.be/share/site-varenv.be?auth=token-varenv&embed=true&theme=light&background=transparent",
        )
        self.assertEqual(
            view.get_embedhostjs_src,
            "https://url-varenv.be/js/embed.host.js",
        )

    @mock.patch.dict(
        os.environ,
        {
            "SMARTWEB_PLAUSIBLE_SITE": "",
            "SMARTWEB_PLAUSIBLE_TOKEN": "",
            "SMARTWEB_PLAUSIBLE_URL": "",
        },
    )
    def test_plausible_view(self):
        view = queryMultiAdapter((self.portal, self.request), name="stats")
        self.assertNotIn("iframe", view())
        self.assertIn("Plausible analytics is not set", view())
        self.set_registry_records()
        self.assertIn("iframe", view())
        self.assertNotIn("Plausible analytics is not set", view())
