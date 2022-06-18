# -*- coding: utf-8 -*-

from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.app.textfield.value import RichTextValue
from zope.component import queryMultiAdapter


class TestSearch(ImioSmartwebTestCase):

    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    def setUp(self):
        """Custom shared utility setup for tests"""
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            id="folder",
        )
        api.content.transition(self.folder, "publish")

    def test_search(self):
        self.request.form["SearchableText"] = "kamoulox"
        search = queryMultiAdapter((self.portal, self.request), name="search")
        self.assertEqual(len(search.results()), 0)

        page = api.content.create(
            container=self.folder,
            type="imio.smartweb.Page",
            title="kamoulox",
        )

        self.assertEqual(len(search.results()), 1)

        section_text = api.content.create(
            container=page,
            type="imio.smartweb.SectionText",
            title="kamoulox",
        )
        section_text.text = RichTextValue("<p>kamoulox</p>", "text/html", "text/html")
        section_text.reindexObject()

        # Some sections (like SectionText) are not searchable
        self.assertEqual(len(search.results()), 1)

        api.content.create(
            container=self.portal,
            type="imio.smartweb.PortalPage",
            title="kamoulox",
        )
        self.assertEqual(len(search.results()), 2)
