# -*- coding: utf-8 -*-

from imio.smartweb.core.interfaces import IImioSmartwebCoreLayer
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import make_named_image
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.namedfile.file import NamedBlobImage
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
        page.image = NamedBlobImage(**make_named_image())
        api.content.transition(page, "publish")
        transaction.commit()

        browser = Browser(self.layer["app"])
        browser.open(self.portal.absolute_url())
        content = browser.contents
        self.assertIn(
            '<meta content="http://nohost/plone/++resource++plone-logo.svg" property="og:image"/>',
            content,
        )
        self.assertIn(
            '<span itemprop="image">http://nohost/plone/++resource++plone-logo.svg</span>',
            content,
        )

        browser.open(folder.absolute_url())
        content = browser.contents
        self.assertIn(
            '<meta content="http://nohost/plone/++resource++plone-logo.svg" property="og:image"/>',
            content,
        )
        self.assertIn(
            '<span itemprop="image">http://nohost/plone/++resource++plone-logo.svg</span>',
            content,
        )

        scales = page.restrictedTraverse("@@images")
        image = scales.scale("image", scale="paysage_vignette")
        browser.open(page.absolute_url())
        content = browser.contents
        self.assertIn(f'<meta content="{image.url}" property="og:image"/>', content)
        self.assertIn(f'<span itemprop="image">{image.url}</span>', content)

        folder.image = NamedBlobImage(**make_named_image())
        transaction.commit()
        scales = folder.restrictedTraverse("@@images")
        image = scales.scale("image", scale="paysage_vignette")
        browser.open(folder.absolute_url())
        content = browser.contents
        self.assertIn(f'<meta content="{image.url}" property="og:image"/>', content)
        self.assertIn(f'<span itemprop="image">{image.url}</span>', content)
