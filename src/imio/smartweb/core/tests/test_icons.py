# -*- coding: utf-8 -*-

from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import make_named_image
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.namedfile.file import NamedBlobImage
from plone.resource.interfaces import IResourceDirectory
from zope.component import getUtility
from zope.component import queryMultiAdapter


class TestIcons(ImioSmartwebTestCase):

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

        link.image = NamedBlobImage(**make_named_image())
        view = queryMultiAdapter((self.page, self.request), name="full_view")()
        self.assertIn(
            "background-image:url('http://nohost/plone/page/links/link/@@images/",
            view,
        )

        link.svg_icon = "view.directory"
        view = queryMultiAdapter((self.page, self.request), name="full_view")()
        self.assertNotIn("background-image", view)
        # svg data (coming from ++plone++imio.smartweb.core/icons/vue-annuaire.svg)
        # we can't get it directly from the file because of all Plone filters
        # that changes the SVG content
        self.assertIn('<path d="M18 0H2V2H18V0ZM2 24H18V22H2V24ZM18', view)

    def test_icons_override(self):
        self.assertVocabularyLen("imio.smartweb.vocabulary.Icons", 49)
        portal_resources = getUtility(IResourceDirectory, name="persistent")
        portal_resources.makeDirectory("plone")
        portal_resources["plone"].makeDirectory("imio.smartweb.core")
        portal_resources["plone"]["imio.smartweb.core"].makeDirectory("icons")
        self.assertVocabularyLen("imio.smartweb.vocabulary.Icons", 0)
        portal_resources.writeFile(
            path="plone/imio.smartweb.core/icons/action-email.svg", data="test"
        )
        self.assertVocabularyLen("imio.smartweb.vocabulary.Icons", 1)
