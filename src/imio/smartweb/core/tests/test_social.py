# -*- coding: utf-8 -*-

from imio.smartweb.core.interfaces import IImioSmartwebCoreLayer
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import get_leadimage_data
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.namedfile.file import NamedBlobFile
from plone.testing.zope import Browser
from zope.interface import alsoProvides

import transaction


class TestSocial(ImioSmartwebTestCase):

    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        alsoProvides(self.request, IImioSmartwebCoreLayer)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_images_urls(self):
        folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            title="Folder",
            id="folder",
        )
        api.content.transition(folder, "publish")
        page = api.content.create(
            container=folder, type="imio.smartweb.Page", title="Page", id="page"
        )
        page.image = NamedBlobFile(data=get_leadimage_data(), filename="plone.png")
        api.content.transition(page, "publish")
        transaction.commit()

        browser = Browser(self.layer["app"])
        browser.open(self.portal.absolute_url())
        content = browser.contents
        self.assertIn(
            '<meta content="http://nohost/plone/logo.png" property="og:image"/>',
            content,
        )
        self.assertIn(
            '<span itemprop="image">http://nohost/plone/logo.png</span>',
            content,
        )

        browser.open(folder.absolute_url())
        content = browser.contents
        self.assertIn(
            '<meta content="http://nohost/plone/logo.png" property="og:image"/>',
            content,
        )
        self.assertIn(
            '<span itemprop="image">http://nohost/plone/logo.png</span>',
            content,
        )

        browser.open(page.absolute_url())
        content = browser.contents
        self.assertIn(
            '<meta content="http://nohost/plone/folder/page/@@images/image/vignette" property="og:image"/>',
            content,
        )
        self.assertIn(
            '<span itemprop="image">http://nohost/plone/folder/page/@@images/image/vignette</span>',
            content,
        )

        folder.image = NamedBlobFile(data=get_leadimage_data(), filename="plone.png")
        transaction.commit()
        browser.open(folder.absolute_url())
        content = browser.contents
        self.assertIn(
            '<meta content="http://nohost/plone/folder/@@images/image/vignette" property="og:image"/>',
            content,
        )
        self.assertIn(
            '<span itemprop="image">http://nohost/plone/folder/@@images/image/vignette</span>',
            content,
        )
