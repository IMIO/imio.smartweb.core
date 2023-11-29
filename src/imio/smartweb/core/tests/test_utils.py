# -*- coding: utf-8 -*-

from freezegun import freeze_time
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import make_named_image
from imio.smartweb.core.utils import batch_results
from imio.smartweb.core.utils import get_scale_url
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.namedfile.file import NamedBlobImage
from plone.uuid.interfaces import IUUID


class TestUtils(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests"""
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_batch_results(self):
        lst = [1, 2, 3, 4, 5, 6]
        self.assertEqual(batch_results(lst, 3), [[1, 2, 3], [4, 5, 6]])
        lst = [1, 2, 3, 4, 5, 6, 7]
        self.assertEqual(batch_results(lst, 3), [[1, 2, 3], [4, 5, 6], [7]])

    @freeze_time("2021-09-14 8:00:00")
    def test_get_scale_url(self):
        content = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            id="page",
        )
        self.assertEqual(
            get_scale_url(content, self.request, "image", "preview", ""), ""
        )
        uuid = IUUID(content)
        brain = api.content.find(UID=uuid)[0]
        self.assertEqual(get_scale_url(brain, self.request, "image", "preview", ""), "")

        content.image = NamedBlobImage(**make_named_image())
        content.reindexObject()
        self.assertIn(
            "http://nohost/plone/page/@@images/image-400-",
            get_scale_url(content, self.request, "image", "preview"),
        )
        paysage_scale = get_scale_url(
            content, self.request, "image", "affiche", "paysage"
        )
        portrait_scale = get_scale_url(
            content, self.request, "image", "affiche", "portrait"
        )
        self.assertIn("http://nohost/plone/page/@@images/image-750-", paysage_scale)
        self.assertIn("http://nohost/plone/page/@@images/image-448-", portrait_scale)
        self.assertNotEqual(paysage_scale, portrait_scale)
        self.assertEqual(
            get_scale_url(content, self.request, "image", "nonexisting"), ""
        )
        self.assertEqual(
            get_scale_url(content, self.request, "nonexisting", "preview"), ""
        )
        self.assertEqual(
            get_scale_url(content, self.request, "image", ""),
            "http://nohost/plone/page/@@images/image/?cache_key=78fd1bab198354b6877aed44e2ea0b4d",
        )
        brain = api.content.find(UID=uuid)[0]
        self.assertEqual(
            get_scale_url(brain, self.request, "image", "preview"),
            "http://nohost/plone/page/@@images/image/preview?cache_key=78fd1bab198354b6877aed44e2ea0b4d",
        )
        self.assertEqual(
            get_scale_url(brain, self.request, "image", "affiche", "paysage"),
            "http://nohost/plone/page/@@images/image/paysage_affiche?cache_key=78fd1bab198354b6877aed44e2ea0b4d",
        )
        self.assertEqual(
            get_scale_url(brain, self.request, "image", "affiche", "portrait"),
            "http://nohost/plone/page/@@images/image/portrait_affiche?cache_key=78fd1bab198354b6877aed44e2ea0b4d",
        )
        self.assertEqual(
            get_scale_url(brain, self.request, "image", "nonexisting"),
            "http://nohost/plone/page/@@images/image/nonexisting?cache_key=78fd1bab198354b6877aed44e2ea0b4d",
        )
        self.assertEqual(
            get_scale_url(brain, self.request, "image", ""),
            "http://nohost/plone/page/@@images/image/?cache_key=78fd1bab198354b6877aed44e2ea0b4d",
        )
        self.assertEqual(
            get_scale_url(brain, self.request, "image", "portrait_affiche", "portrait"),
            "http://nohost/plone/page/@@images/image/portrait_affiche?cache_key=78fd1bab198354b6877aed44e2ea0b4d",
        )
