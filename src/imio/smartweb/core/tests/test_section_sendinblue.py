# -*- coding: utf-8 -*-

from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import queryMultiAdapter


class TestSectionNews(ImioSmartwebTestCase):

    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    def setUp(self):
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portalpage = api.content.create(
            container=self.portal,
            type="imio.smartweb.PortalPage",
            id="Portal page",
        )

    def test_button_position(self):
        section_sendinblue = api.content.create(
            container=self.portalpage,
            type="imio.smartweb.SectionSendinblue",
            title="SendInBlue",
        )
        section_view = queryMultiAdapter(
            (section_sendinblue, self.request), name="view"
        )
        self.assertEqual(section_view.button_position, "button_bottom")

        portal_page_view = queryMultiAdapter(
            (self.portalpage, self.request), name="full_view"
        )
        self.assertIn("button_bottom", portal_page_view())

        api.portal.set_registry_record(
            "smartweb.sendinblue_button_position", "button_right"
        )
        portal_page_view = queryMultiAdapter(
            (self.portalpage, self.request), name="full_view"
        )
        self.assertIn("button_right", portal_page_view())

    def test_button_text(self):
        section_sendinblue = api.content.create(
            container=self.portalpage,
            type="imio.smartweb.SectionSendinblue",
            title="SendInBlue",
        )
        section_view = queryMultiAdapter(
            (section_sendinblue, self.request), name="view"
        )
        self.assertEqual(section_view.button_text, "Subscribe")

        portal_page_view = queryMultiAdapter(
            (self.portalpage, self.request), name="full_view"
        )
        self.assertIn('value="Subscribe"', portal_page_view())

        texts = [
            {"language": "fr", "text": "Je m'inscris!"},
            {"language": "en", "text": "Register!"},
        ]
        api.portal.set_registry_record("smartweb.sendinblue_button_text", texts)
        portal_page_view = queryMultiAdapter(
            (self.portalpage, self.request), name="full_view"
        )
        self.assertNotIn('value="Subscribe"', portal_page_view())
        self.assertIn('value="Register!"', portal_page_view())
