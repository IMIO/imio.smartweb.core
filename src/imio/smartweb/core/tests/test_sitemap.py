# -*- coding: utf-8 -*-

from freezegun import freeze_time
from gzip import GzipFile
from io import BytesIO
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
from zope.component import getMultiAdapter

import json
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
        self.assertIn("<lastmod >2024-02-02T08:00:00+00:00</lastmod>", xml)
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
        self.assertIn(
            "<loc>http://nohost/plone/folder/page1/gallery/image/view</loc>", xml
        )
        # Gallery and image created 2024-02-02 10:00:00
        self.assertIn(
            "<loc>http://nohost/plone/folder/page1/gallery/image/view</loc>\n    <lastmod >2024-02-02T10:00:00+00:00</lastmod>",
            xml,
        )

        rest_views = {
            "directory": self.rest_directory,
            "events": self.rest_agenda,
            "news": self.rest_news,
        }
        for k, v in rest_views.items():
            api.portal.set_registry_record(f"smartweb.default_{k}_view", v.UID())

        self.json_contacts = get_json("resources/json_contacts_raw_mock.json")
        self.json_news = get_json("resources/json_rest_news.json")
        self.json_events = get_json("resources/json_rest_events.json")

        contact_search_url = "http://localhost:8080/Plone/@search?selected_entities=396907b3b1b04a97896b12cc792c77f8&portal_type=imio.directory.Contact&fullobjects=0&sort_on=sortable_title"
        news_search_url = f"http://localhost:8080/Plone/@search?selected_news_folders={self.rest_news.selected_news_folder}&portal_type=imio.news.NewsItem&fullobjects=0&sort_on=sortable_title"
        events_search_url = f"http://localhost:8080/Plone/@events?selected_agendas={self.rest_agenda.selected_agenda}&portal_type=imio.events.Event&fullobjects=0&sort_on=sortable_title"

        m.get(contact_search_url, text=json.dumps(self.json_contacts))
        m.get(news_search_url, text=json.dumps(self.json_news))
        m.get(events_search_url, text=json.dumps(self.json_events))

        sitemap = getMultiAdapter(
            (self.portal, self.portal.REQUEST), name="sitemap.xml.gz"
        )
        xml = self.uncompress(sitemap())
        self.assertIn("<loc>http://nohost/plone/directory-view/contact1-title", xml)
        self.assertIn("<loc>http://nohost/plone/news-view/", xml)
        self.assertIn("<loc>http://nohost/plone/agenda-view/", xml)

    def uncompress(self, sitemapdata):
        sio = BytesIO(sitemapdata)
        unzipped = GzipFile(fileobj=sio)
        xml = unzipped.read()
        unzipped.close()
        return safe_text(xml)
