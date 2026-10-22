# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta
from datetime import timezone
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.memoize.ram import choose_cache
from z3c.caching.interfaces import ILastModified
from zope.component import queryMultiAdapter

import requests_mock

NEWS_FOLDER_UID = "64f4cbee9a394a018a951f6d94452914"
LIGHT_QUERY_URL = (
    "http://localhost:8080/Plone/@search_newsitems"
    f"?selected_news_folders={NEWS_FOLDER_UID}&sort_on=modified&sort_limit=1"
)


class TestPagesLastModified(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portalpage = api.content.create(
            container=self.portal,
            type="imio.smartweb.PortalPage",
            id="portalpage",
        )

    def last_modified(self):
        choose_cache(
            "imio.smartweb.core.contents.pages.caching._latest_news_modification"
        ).ramcache.invalidateAll()
        view = queryMultiAdapter((self.portalpage, self.request), name="full_view")
        return ILastModified(view)()

    @requests_mock.Mocker()
    def test_call(self, m):
        page_modified = self.portalpage.modified().asdatetime()
        self.assertEqual(self.last_modified(), page_modified)

        news = api.content.create(
            container=self.portalpage,
            type="imio.smartweb.SectionNews",
            title="My news",
        )
        news.related_news = NEWS_FOLDER_UID
        page_modified = self.portalpage.modified().asdatetime()

        recent = (page_modified + timedelta(minutes=5)).astimezone(timezone.utc)
        m.get(LIGHT_QUERY_URL, json={"items": [{"modified": recent.isoformat()}]})
        self.assertEqual(self.last_modified(), recent)
        # the page itself is not modified (no ZODB write)
        self.assertEqual(self.portalpage.modified().asdatetime(), page_modified)

        old = datetime(2023, 5, 22, 8, 51, 55, tzinfo=timezone.utc)
        m.get(LIGHT_QUERY_URL, json={"items": [{"modified": old.isoformat()}]})
        self.assertEqual(self.last_modified(), page_modified)

        m.get(LIGHT_QUERY_URL, json={"items": []})
        self.assertEqual(self.last_modified(), page_modified)

        m.get(LIGHT_QUERY_URL, status_code=500)
        self.assertEqual(self.last_modified(), page_modified)

        news.specific_related_newsitems = ["bfe2b4391a0f4a8db6d8b7fed63d1c4a"]
        m.get(
            "http://localhost:8080/Plone/@search_newsitems"
            "?UID=bfe2b4391a0f4a8db6d8b7fed63d1c4a&sort_on=modified",
            json={"items": [{"modified": recent.isoformat()}]},
        )
        self.assertEqual(self.last_modified(), recent)
