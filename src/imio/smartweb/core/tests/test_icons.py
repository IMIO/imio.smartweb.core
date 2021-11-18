# -*- coding: utf-8 -*-

from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.namedfile.file import NamedBlobFile
from zope.component import queryMultiAdapter


class TestSections(ImioSmartwebTestCase):

    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.page = api.content.create(
            container=self.portal, type="imio.smartweb.Page", id="page"
        )
        self.section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionLinks",
            id="links",
        )

    def test_link_icon(self):
        link = api.content.create(
            container=self.section,
            type="imio.smartweb.BlockLink",
            id="link",
        )
        link.remoteUrl = "https://www.imio.be"
        view = queryMultiAdapter((self.page, self.request), name="full_view")()
        self.assertNotIn("background-image", view)
        self.assertNotIn("<svg", view)

        link.image = NamedBlobFile(data="file data", filename=u"file.png")
        view = queryMultiAdapter((self.page, self.request), name="full_view")()
        self.assertIn(
            "background-image:url('http://nohost/plone/page/links/link/@@images/image/vignette')",
            view,
        )
        self.assertNotIn("<svg", view)

        link.svg_icon = "annuaire"
        view = queryMultiAdapter((self.page, self.request), name="full_view")()
        self.assertNotIn("background-image", view)
        self.assertIn("<svg", view)
