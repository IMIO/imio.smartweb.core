# -*- coding: utf-8 -*-

from freezegun import freeze_time
from gzip import GzipFile
from io import BytesIO
from imio.smartweb.core.browser.sitemap import CatalogSiteMap
from imio.smartweb.core.browser.sitemap import get_endpoint_data
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import get_json
from imio.smartweb.core.tests.utils import make_named_image
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.textfield.value import RichTextValue
from plone.base.utils import safe_text
from plone.memoize.ram import choose_cache
from plone.namedfile.file import NamedBlobImage
from unittest.mock import patch
from unittest.mock import Mock
from zope.component import getMultiAdapter

import requests_mock


class TestPage(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    @freeze_time("2024-02-02 8:00:00")
    def setUp(self):
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        api.portal.set_registry_record("plone.enable_sitemap", True)

        self.default_page = api.content.create(
            container=self.portal,
            type="imio.smartweb.PortalPage",
            title="Portal page",
            id="portal-page",
        )
        self.portal.setDefaultPage("portal-page")

        self.folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            title="Folder",
            id="folder",
        )
        self.page = api.content.create(
            container=self.folder,
            type="imio.smartweb.Page",
            title="Page 1",
            id="page1",
        )
        self.section_text = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionText",
            title="Section text",
        )
        self.section_text.text = RichTextValue(
            "<p>Kamoulox</p>", "text/html", "text/html"
        )

        self.rest_directory = api.content.create(
            container=self.portal,
            type="imio.smartweb.DirectoryView",
            title="directory view",
        )
        self.rest_agenda = api.content.create(
            container=self.portal,
            type="imio.smartweb.EventsView",
            title="agenda view",
        )
        self.rest_agenda.selected_agenda = "64f4cbee9a394a018a951f6d94452914"
        self.rest_news = api.content.create(
            container=self.portal,
            type="imio.smartweb.NewsView",
            title="news view",
        )
        self.rest_news.selected_news_folder = "64f4cbee9a394a018a951f6d94452914"
        self.json_rest_directory = get_json("resources/json_rest_directory.json")
        self.json_rest_events = get_json("resources/json_rest_events.json")
        self.json_rest_news = get_json("resources/json_rest_news.json")

        api.content.transition(self.rest_directory, "publish")
        api.content.transition(self.rest_agenda, "publish")
        api.content.transition(self.rest_news, "publish")

    # 'http://localhost:8080/Plone/@search?selected_entities=396907b3b1b04a97896b12cc792c77f8&portal_type=imio.directory.Contact&fullobjects=0&sort_on=sortable_title'
    @freeze_time("2024-02-02 10:00:00")
    @patch(
        "imio.smartweb.core.contents.rest.news.endpoint.BaseNewsEndpoint._get_news_folders_uids_and_title_from_entity",
        return_value=(
            ["64f4cbee9a394a018a951f6d94452914"],
            {"64f4cbee9a394a018a951f6d94452914": "News Folder title"},
        ),
    )
    @requests_mock.Mocker()
    def test_sitemap(self, mock_news, m):
        sitemap = getMultiAdapter(
            (self.portal, self.portal.REQUEST), name="sitemap.xml.gz"
        )
        xml = self.uncompress(sitemap())
        self.assertIn("<lastmod >2024-02-02T08:00:00", xml)
        self.assertIn("<loc>http://nohost/plone/folder</loc>", xml)
        self.assertIn("http://nohost/plone/folder/page1", xml)
        self.assertNotIn(
            "<loc>http://nohost/plone/folder/page1/gallery/image/view</loc>", xml
        )

        # Gallery and image created 2024-02-02 10:00:00
        gallery = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionGallery",
            title="Gallery",
        )
        image = api.content.create(
            container=gallery,
            type="Image",
            title="Image",
        )
        image.image = NamedBlobImage(**make_named_image())
        sitemap = getMultiAdapter(
            (self.portal, self.portal.REQUEST), name="sitemap.xml.gz"
        )
        xml = self.uncompress(sitemap())
        self.assertIn("<loc>http://nohost/plone/folder/page1/gallery/image</loc>", xml)
        # Gallery and image created 2024-02-02 10:00:00
        self.assertIn(
            "<loc>http://nohost/plone/folder/page1/gallery/image</loc>\n    <lastmod >2024-02-02T10:00:00",
            xml,
        )

        cache = choose_cache("imio.smartweb.core.browser.sitemap.get_endpoint_data")
        cache.ramcache.invalidateAll()

        with patch(
            "imio.smartweb.core.contents.rest.news.endpoint.BaseNewsEndpoint.__call__",
            return_value=self.json_rest_news,
        ):
            xml = self.uncompress(sitemap())
            self.assertIn(
                "<loc>http://nohost/plone/news-view/ceci-est-une-deuxieme-actualite",
                xml,
            )

        cache = choose_cache("imio.smartweb.core.browser.sitemap.get_endpoint_data")
        cache.ramcache.invalidateAll()

        with patch(
            "imio.smartweb.core.contents.rest.directory.endpoint.BaseDirectoryEndpoint.__call__",
            return_value=self.json_rest_directory,
        ):
            xml = self.uncompress(sitemap())
            self.assertIn(
                "<loc>http://nohost/plone/directory-view/service-communication-de-ladministration-communale",
                xml,
            )

        cache = choose_cache("imio.smartweb.core.browser.sitemap.get_endpoint_data")
        cache.ramcache.invalidateAll()

        with patch(
            "imio.smartweb.core.contents.rest.events.endpoint.BaseEventsEndpoint.__call__",
            return_value=self.json_rest_events,
        ):
            xml = self.uncompress(sitemap())
            self.assertIn(
                "<loc>http://nohost/plone/agenda-view/evenement-recurrent-tous-les-samedi",
                xml,
            )

    @patch(
        "imio.smartweb.core.contents.rest.news.endpoint.BaseNewsEndpoint._get_news_folders_uids_and_title_from_entity",
        return_value=(
            ["64f4cbee9a394a018a951f6d94452914"],
            {"64f4cbee9a394a018a951f6d94452914": "News Folder title"},
        ),
    )
    def test_site_map_for_user_display(self, mock_news):
        # Keep the "empty source" assertions hermetic: without mocking, the
        # remote calls would reach a live DIRECTORY_URL/EVENTS_URL/NEWS_URL
        # instance if one happens to run (e.g. a dev server on :8080), which
        # returns a truthy response and adds a spurious seo entry, breaking
        # "0 children". Mock external HTTP only (plone-testing R1).
        with (
            patch(
                "imio.smartweb.core.contents.rest.directory.endpoint.BaseDirectoryEndpoint.__call__",
                return_value={},
            ),
            patch(
                "imio.smartweb.core.contents.rest.events.endpoint.BaseEventsEndpoint.__call__",
                return_value={},
            ),
            patch(
                "imio.smartweb.core.contents.rest.news.endpoint.BaseNewsEndpoint.__call__",
                return_value={},
            ),
        ):
            sitemap = CatalogSiteMap(self.portal, self.request)
            # 3 authentic sources
            self.assertEqual(len(sitemap.siteMap().get("children")), 3)
            self.assertNotIn(
                "Folder",
                [child.get("Title") for child in sitemap.siteMap().get("children")],
            )

            # Publish folder and page (private content don't appear in sitemap)
            api.content.transition(self.folder, "publish")
            api.content.transition(self.page, "publish")
            sitemap = CatalogSiteMap(self.portal, self.request)
            self.assertEqual(len(sitemap.siteMap().get("children")), 4)
            self.assertIn(
                "Folder",
                [child.get("Title") for child in sitemap.siteMap().get("children")],
            )
            folder_entry = [
                child
                for child in sitemap.siteMap().get("children")
                if child.get("Title") == "Folder"
            ][0]
            self.assertIn(
                "Page 1",
                [child.get("Title") for child in folder_entry.get("children")],
            )

            directory_entry = [
                child
                for child in sitemap.siteMap().get("children")
                if child.get("Title") == "directory view"
            ][0]
            self.assertEqual(len(directory_entry.get("children")), 0)

        cache = choose_cache("imio.smartweb.core.browser.sitemap.get_endpoint_data")
        cache.ramcache.invalidateAll()

        # Populate directory view with 6 contacts
        with patch(
            "imio.smartweb.core.contents.rest.directory.endpoint.BaseDirectoryEndpoint.__call__",
            return_value=self.json_rest_directory,
        ):
            sitemap = CatalogSiteMap(self.portal, self.request)
            directory_entry = [
                child
                for child in sitemap.siteMap().get("children")
                if child.get("Title") == "directory view"
            ][0]
            self.assertEqual(len(directory_entry.get("children")), 7)

    def test_bad_portal_type(self):
        obj = Mock()
        obj.portal_type = None
        request = Mock()
        result = get_endpoint_data(obj, request, 50, None, None)
        assert result == {}

    def test_get_filter_sort(self):
        from imio.smartweb.core.browser.sitemap import get_filter_sort

        self.assertEqual(
            get_filter_sort("imio.smartweb.DirectoryView", "most_recent"),
            ("created", "descending"),
        )
        self.assertEqual(
            get_filter_sort("imio.smartweb.NewsView", "most_recent"),
            (None, None),
        )
        self.assertEqual(
            get_filter_sort("imio.smartweb.EventsView", "most_recent"),
            (None, None),
        )

    def test_get_sitemap_sources_config_fallback(self):
        from imio.smartweb.core.browser.sitemap import (
            get_sitemap_sources_config,
        )

        with patch(
            "imio.smartweb.core.browser.sitemap.api.portal.get_registry_record",
            return_value=None,
        ):
            config = get_sitemap_sources_config()
        self.assertEqual(
            set(config),
            {
                "imio.smartweb.EventsView",
                "imio.smartweb.NewsView",
                "imio.smartweb.DirectoryView",
            },
        )
        for cfg in config.values():
            self.assertTrue(cfg["enabled"])
            self.assertEqual(cfg["max_items"], 50)
            self.assertEqual(cfg["item_filter"], "most_recent")

    @patch(
        "imio.smartweb.core.contents.rest.news.endpoint.BaseNewsEndpoint._get_news_folders_uids_and_title_from_entity",
        return_value=(
            ["64f4cbee9a394a018a951f6d94452914"],
            {"64f4cbee9a394a018a951f6d94452914": "News Folder title"},
        ),
    )
    def test_site_map_html_respects_enabled(self, mock_news):
        # Disable Directory -> its remote items are not expanded even when the
        # endpoint returns contacts.
        api.portal.set_registry_record(
            "smartweb.sitemap_authentic_sources",
            [
                {
                    "source_type": "imio.smartweb.EventsView",
                    "enabled": True,
                    "max_items": 50,
                    "item_filter": "most_recent",
                },
                {
                    "source_type": "imio.smartweb.NewsView",
                    "enabled": True,
                    "max_items": 50,
                    "item_filter": "most_recent",
                },
                {
                    "source_type": "imio.smartweb.DirectoryView",
                    "enabled": False,
                    "max_items": 50,
                    "item_filter": "most_recent",
                },
            ],
        )
        cache = choose_cache("imio.smartweb.core.browser.sitemap.get_endpoint_data")
        cache.ramcache.invalidateAll()
        with patch(
            "imio.smartweb.core.contents.rest.directory.endpoint.BaseDirectoryEndpoint.__call__",
            return_value=self.json_rest_directory,
        ):
            sitemap = CatalogSiteMap(self.portal, self.request)
            directory_entry = [
                c
                for c in sitemap.siteMap().get("children")
                if c.get("Title") == "directory view"
            ][0]
            self.assertEqual(len(directory_entry.get("children")), 0)

    @patch(
        "imio.smartweb.core.contents.rest.news.endpoint.BaseNewsEndpoint._get_news_folders_uids_and_title_from_entity",
        return_value=(
            ["64f4cbee9a394a018a951f6d94452914"],
            {"64f4cbee9a394a018a951f6d94452914": "News Folder title"},
        ),
    )
    def test_site_map_html_caps_max_items(self, mock_news):
        # Directory endpoint returns several contacts; max_items=2 caps to 2.
        api.portal.set_registry_record(
            "smartweb.sitemap_authentic_sources",
            [
                {
                    "source_type": "imio.smartweb.EventsView",
                    "enabled": True,
                    "max_items": 50,
                    "item_filter": "most_recent",
                },
                {
                    "source_type": "imio.smartweb.NewsView",
                    "enabled": True,
                    "max_items": 50,
                    "item_filter": "most_recent",
                },
                {
                    "source_type": "imio.smartweb.DirectoryView",
                    "enabled": True,
                    "max_items": 2,
                    "item_filter": "most_recent",
                },
            ],
        )
        cache = choose_cache("imio.smartweb.core.browser.sitemap.get_endpoint_data")
        cache.ramcache.invalidateAll()
        with patch(
            "imio.smartweb.core.contents.rest.directory.endpoint.BaseDirectoryEndpoint.__call__",
            return_value=self.json_rest_directory,
        ):
            sitemap = CatalogSiteMap(self.portal, self.request)
            directory_entry = [
                c
                for c in sitemap.siteMap().get("children")
                if c.get("Title") == "directory view"
            ][0]
            # format_sitemap_items appends one extra "seo_html" entry, so a
            # 2-item cap yields 2 items + 1 seo entry = 3 children.
            self.assertEqual(len(directory_entry.get("children")), 3)

    def test_sitemap_sources_config_default(self):
        rows = api.portal.get_registry_record("smartweb.sitemap_authentic_sources")
        self.assertEqual(len(rows), 3)
        by_type = {r["source_type"]: r for r in rows}
        self.assertEqual(
            set(by_type),
            {
                "imio.smartweb.EventsView",
                "imio.smartweb.NewsView",
                "imio.smartweb.DirectoryView",
            },
        )
        for row in rows:
            self.assertTrue(row["enabled"])
            self.assertEqual(row["max_items"], 50)
            self.assertEqual(row["item_filter"], "most_recent")

    @patch(
        "imio.smartweb.core.contents.rest.news.endpoint.BaseNewsEndpoint."
        "_get_news_folders_uids_and_title_from_entity",
        return_value=(
            ["64f4cbee9a394a018a951f6d94452914"],
            {"64f4cbee9a394a018a951f6d94452914": "News Folder title"},
        ),
    )
    def test_endpoint_sort_override(self, mock_news):
        from imio.smartweb.core.contents.rest.directory.endpoint import (
            DirectoryEndpoint,
        )
        from imio.smartweb.core.contents.rest.events.endpoint import EventsEndpoint
        from imio.smartweb.core.contents.rest.news.endpoint import NewsEndpoint

        # Directory: default alphabetical, overridable to created/descending.
        ep = DirectoryEndpoint(self.rest_directory, self.request)
        self.assertIn("sort_on=sortable_title", ep.query_url)
        ep = DirectoryEndpoint(
            self.rest_directory,
            self.request,
            sort_on="created",
            sort_order="descending",
        )
        url = ep.query_url
        self.assertIn("sort_on=created", url)
        self.assertIn("sort_order=descending", url)
        self.assertNotIn("sort_on=sortable_title", url)

        # Events: native event_dates preserved when no override.
        ep = EventsEndpoint(self.rest_agenda, self.request)
        self.assertIn("sort_on=event_dates", ep.query_url)

        # News: native effective/descending preserved when no override.
        ep = NewsEndpoint(self.rest_news, self.request)
        self.assertIn("sort_on=effective", ep.query_url)
        self.assertIn("sort_order=descending", ep.query_url)

    def test_sitemap_source_type_is_not_display_mode(self):
        # Regression: source_type was declared mode="display". A display-mode
        # column is not submitted, so DictRow validation rejected every row on
        # save ("Le système n'a pas pu traiter la valeur fournie" / "Champ
        # obligatoire"). It must stay a real (input) widget so its per-row
        # value is posted and survives extraction.
        from imio.smartweb.core.browser.controlpanel_siteadmin import (
            ISitemapSourceRowSchema,
        )
        from plone.autoform.interfaces import MODES_KEY

        modes = ISitemapSourceRowSchema.queryTaggedValue(MODES_KEY, [])
        display_fields = [name for _, name, mode in modes if mode == "display"]
        self.assertNotIn("source_type", display_fields)

    def test_frozen_label_widget_renders_full_token(self):
        # The Source column widget renders a read-only label (the term title)
        # plus a hidden input carrying the FULL token, whether the DataGrid
        # feeds it a raw token string or a list of tokens. Regression:
        # self.value[0] on a string rendered a single character ("i") as both
        # label and submitted value.
        from imio.smartweb.core.browser.controlpanel_siteadmin import (
            FrozenLabelFieldWidget,
        )
        from imio.smartweb.core.browser.controlpanel_siteadmin import (
            ISitemapSourceRowSchema,
        )
        from z3c.form.testing import TestRequest

        field = ISitemapSourceRowSchema["source_type"].bind(self.portal)

        # Raw token string (what the DataGrid object widget actually feeds).
        widget = FrozenLabelFieldWidget(field, TestRequest())
        widget.update()
        widget.value = "imio.smartweb.NewsView"
        html = widget.render()
        self.assertIn('value="imio.smartweb.NewsView"', html)
        self.assertNotIn('value="i"', html)
        self.assertIn("Actualités", html)

        # List of tokens (what a stand-alone SelectWidget holds).
        widget = FrozenLabelFieldWidget(field, TestRequest())
        widget.update()
        widget.value = ["imio.smartweb.EventsView"]
        html = widget.render()
        self.assertIn('value="imio.smartweb.EventsView"', html)
        self.assertIn("Agenda", html)

    def test_sitemap_config_guard_rejects_incomplete_source_set(self):
        # The applyChanges guard must reject a grid that does not list each
        # authentic source exactly once (protects against an edited/duplicated
        # source_type now that the column is an editable Choice).
        from imio.smartweb.core.browser.controlpanel_siteadmin import (
            SmartwebSiteAdminControlPanelForm,
        )

        form = SmartwebSiteAdminControlPanelForm(self.portal, self.request)
        incomplete = [
            {
                "source_type": "imio.smartweb.EventsView",
                "enabled": True,
                "max_items": 50,
                "item_filter": "most_recent",
            },
            {
                "source_type": "imio.smartweb.NewsView",
                "enabled": True,
                "max_items": 50,
                "item_filter": "most_recent",
            },
        ]
        result = form.applyChanges({"sitemap_authentic_sources": incomplete})
        self.assertFalse(result)

    def uncompress(self, sitemapdata):
        sio = BytesIO(sitemapdata)
        unzipped = GzipFile(fileobj=sio)
        xml = unzipped.read()
        unzipped.close()
        return safe_text(xml)
