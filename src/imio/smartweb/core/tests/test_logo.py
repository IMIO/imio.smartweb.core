# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import make_named_image
from imio.smartweb.core.viewlets.logo import label_svg
from imio.smartweb.core.viewlets.logo import LogoViewlet
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.formwidget.namedfile.converter import b64encode_file
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.interfaces import ISiteSchema
from zope.component import getUtility


class TestLogo(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests"""
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_portal_logo(self):
        viewlet = LogoViewlet(self.portal, self.request, None, None)
        viewlet.update()
        self.assertFalse(viewlet.show_title)
        self.assertTrue(viewlet.show_logo)
        self.assertFalse(viewlet.is_svg)
        self.assertEqual(viewlet.navigation_root_url, "http://nohost/plone")
        html = viewlet.render()
        soup = BeautifulSoup(html)
        img = soup.find("img")
        self.assertEqual(
            img.get("src"), "http://nohost/plone/++resource++plone-logo.svg"
        )
        link = soup.find("a", id="portal-logo")
        self.assertEqual(link.get("aria-label"), "Back to Plone site homepage")
        self.assertEqual(link.get("title"), "Back to Plone site homepage")
        self.assertEqual(img.get("alt"), "Plone site")
        self.assertEqual(img.get("title"), "Back to Plone site homepage")

        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISiteSchema, prefix="plone")
        encoded_data = b64encode_file(**make_named_image("plone.svg"))
        settings.site_logo = encoded_data
        viewlet.update()
        self.assertTrue(viewlet.show_logo)
        self.assertTrue(viewlet.is_svg)
        self.assertIn(b"<svg", viewlet.svg_data)
        html = viewlet.render()
        soup = BeautifulSoup(html)
        img = soup.find("img")
        self.assertIsNone(img)
        svg = soup.find("svg")
        self.assertEqual(svg.get("role"), "img")
        self.assertEqual(svg.get("aria-label"), "Back to Plone site homepage")
        self.assertEqual(svg.find("title").text, "Back to Plone site homepage")

        encoded_data = b64encode_file(**make_named_image())
        settings.site_logo = encoded_data
        viewlet = LogoViewlet(self.portal, self.request, None, None)
        viewlet.update()
        self.assertTrue(viewlet.show_logo)
        self.assertFalse(viewlet.is_svg)
        html = viewlet.render()
        soup = BeautifulSoup(html)
        img = soup.find("img")
        self.assertEqual(img.get("src"), "http://nohost/plone/@@site-logo/plone.png")

    def test_label_svg(self):
        svg = label_svg(
            b'<svg xmlns="http://www.w3.org/2000/svg"><title>Old</title></svg>',
            "Back to Plone site homepage",
        )
        soup = BeautifulSoup(svg)
        titles = soup.find_all("title")
        self.assertEqual(len(titles), 1)
        self.assertEqual(titles[0].text, "Back to Plone site homepage")

        self.assertEqual(label_svg(b"<svg>not xml", "label"), b"<svg>not xml")
