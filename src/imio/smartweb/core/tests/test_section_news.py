# -*- coding: utf-8 -*-

from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.component import queryMultiAdapter
from zope.intid.interfaces import IIntIds

import requests_mock


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

    @requests_mock.Mocker()
    def test_news(self, m):
        rest_news_view = api.content.create(
            container=self.portal,
            type="imio.smartweb.NewsView",
            title="Rest news view",
        )
        news = api.content.create(
            container=self.portalpage,
            type="imio.smartweb.SectionNews",
            title="My news",
        )
        intids = getUtility(IIntIds)
        news.related_news = "64f4cbee9a394a018a951f6d94452914"
        news.linking_rest_view = RelationValue(intids.getId(rest_news_view))
        news.link_text = "Voir toutes les actualités"
        view = queryMultiAdapter((self.portalpage, self.request), name="full_view")
        self.assertIn("My news", view())
        news_view = queryMultiAdapter((news, self.request), name="carousel_view")
        self.assertEqual(news_view.items, [])
