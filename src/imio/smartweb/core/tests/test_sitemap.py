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
    @requests_mock.Mocker()
    def test_sitemap(self, m):
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
        with patch(
            "imio.smartweb.core.contents.rest.news.endpoint.BaseNewsEndpoint.__call__",
            return_value=self.json_rest_news,
        ) as mypatch:
            xml = self.uncompress(sitemap())
            self.assertIn(
                "<loc>http://nohost/plone/news-view/ceci-est-une-deuxieme-actualite",
                xml,
            )
        with patch(
            "imio.smartweb.core.contents.rest.directory.endpoint.BaseDirectoryEndpoint.__call__",
            return_value=self.json_rest_directory,
        ) as mypatch:
            xml = self.uncompress(sitemap())
            self.assertIn(
                "<loc>http://nohost/plone/directory-view/service-communication-de-ladministration-communale",
                xml,
            )
        with patch(
            "imio.smartweb.core.contents.rest.events.endpoint.BaseEventsEndpoint.__call__",
            return_value=self.json_rest_events,
        ):
            xml = self.uncompress(sitemap())
            self.assertIn(
                "<loc>http://nohost/plone/agenda-view/evenement-recurrent-tous-les-samedi",
                xml,
            )

    def test_site_map_for_user_display(self):
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
            "Page 1", [child.get("Title") for child in folder_entry.get("children")]
        )

        directory_entry = [
            child
            for child in sitemap.siteMap().get("children")
            if child.get("Title") == "directory view"
        ][0]
        self.assertEqual(len(directory_entry.get("children")), 0)

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
            self.assertEqual(len(directory_entry.get("children")), 6)

    def test_bad_portal_type(self):
        obj = Mock()
        obj.portal_type = None
        request = Mock()
        result = get_endpoint_data(obj, request)
        assert result == {}

    def uncompress(self, sitemapdata):
        sio = BytesIO(sitemapdata)
        unzipped = GzipFile(fileobj=sio)
        xml = unzipped.read()
        unzipped.close()
        return safe_text(xml)
