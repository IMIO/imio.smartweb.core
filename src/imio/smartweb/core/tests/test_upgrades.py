# -*- coding: utf-8 -*-

from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.upgrades.upgrades import set_sections_source_from_specific_items
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID


class TestUpgrades(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portalpage = api.content.create(
            container=self.portal,
            type="imio.smartweb.PortalPage",
            id="portal-page",
        )

    def test_set_sections_source_from_specific_items(self):
        agenda_section = api.content.create(
            container=self.portalpage,
            type="imio.smartweb.SectionEvents",
            title="From an agenda",
        )
        agenda_section.related_events = "e73e6a81afea4a579cd0da2773af8d29"
        picked_events_section = api.content.create(
            container=self.portalpage,
            type="imio.smartweb.SectionEvents",
            title="Hand-picked events",
        )
        picked_events_section.specific_related_events = [
            "1178188bddde4ced95a6cf8bf04c443c"
        ]
        newsfolder_section = api.content.create(
            container=self.portalpage,
            type="imio.smartweb.SectionNews",
            title="From a news folder",
        )
        newsfolder_section.related_news = "64f4cbee9a394a018a951f6d94452914"
        picked_news_section = api.content.create(
            container=self.portalpage,
            type="imio.smartweb.SectionNews",
            title="Hand-picked news items",
        )
        picked_news_section.specific_related_newsitems = [
            "bfe2b4391a0f4a8db6d8b7fed63d1c4a"
        ]

        # This is why the step is needed: content predating the source field
        # stores nothing, so it silently reads the field default and the
        # hand-picked sections would fall back to their (unused) container.
        self.assertEqual(picked_events_section.events_source, "agenda")
        self.assertEqual(picked_news_section.news_source, "newsfolder")

        set_sections_source_from_specific_items(None)

        self.assertEqual(picked_events_section.events_source, "selection")
        self.assertEqual(picked_news_section.news_source, "selection")
        # sections listing a whole container are left on their container source
        self.assertEqual(agenda_section.events_source, "agenda")
        self.assertEqual(newsfolder_section.news_source, "newsfolder")
