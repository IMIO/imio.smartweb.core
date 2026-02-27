# -*- coding: utf-8 -*-

from freezegun import freeze_time
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import make_named_image
from imio.smartweb.core.utils import batch_results
from imio.smartweb.core.utils import get_plausible_vars
from imio.smartweb.core.utils import get_scale_url
from imio.smartweb.core.utils import get_ts_api_url
from imio.smartweb.core.utils import is_valid_url
from imio.smartweb.core.utils import populate_procedure_button_text
from imio.smartweb.core.utils import remove_cache_key
from imio.smartweb.core.tests.utils import get_json
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.namedfile.file import NamedBlobImage
from plone.registry.interfaces import IRegistry
from plone.uuid.interfaces import IUUID
from unittest.mock import patch
from zope.component import getUtility


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

    def test_remove_cache_key(self):
        self.json_news = get_json("resources/json_news_raw_mock.json")
        self.assertIn("cache_key", self.json_news["@id"])
        for key in ["@id", "first", "last", "next"]:
            if key in self.json_news["batching"] and isinstance(
                self.json_news["batching"][key], str
            ):
                self.assertIn("cache_key", self.json_news["batching"][key])
        self.json_news = remove_cache_key(self.json_news)

        self.assertNotIn("cache_key", self.json_news["@id"])
        for key in ["@id", "first", "last", "next"]:
            if key in self.json_news["batching"] and isinstance(
                self.json_news["batching"][key], str
            ):
                self.assertNotIn("cache_key", self.json_news["batching"][key])

    def test_remove_cache_key_none(self):
        result = remove_cache_key(None)
        self.assertIsNone(result)

    def test_is_valid_url(self):
        self.assertTrue(is_valid_url("https://kamoulox.be"))
        self.assertTrue(is_valid_url("http://www.kamoulox.be/path?q=1"))
        self.assertFalse(is_valid_url("not-a-url"))
        self.assertFalse(is_valid_url("ftp://kamoulox.be"))
        self.assertFalse(is_valid_url(""))

    def test_get_ts_api_url_no_registry_value(self):
        # When registry value is None, returns None
        with patch("imio.smartweb.core.utils.get_value_from_registry") as mock_registry:
            mock_registry.return_value = None
            result = get_ts_api_url("wcs")
            self.assertIsNone(result)

    def test_get_ts_api_url_invalid_url(self):
        with patch("imio.smartweb.core.utils.get_value_from_registry") as mock_registry:
            mock_registry.return_value = "not-a-valid-url"
            result = get_ts_api_url("wcs")
            self.assertIsNone(result)

    def test_get_ts_api_url_valid_url(self):
        with patch("imio.smartweb.core.utils.get_value_from_registry") as mock_registry:
            mock_registry.return_value = "https://mysite.guichet-citoyen.be"
            result = get_ts_api_url("wcs")
            self.assertIsNotNone(result)
            self.assertIn("-formulaires.guichet-citoyen.be", result)
            self.assertIn("/api", result)

    def test_get_plausible_vars_not_set(self):
        # By default, registry values are None, so get_plausible_vars returns None
        result = get_plausible_vars()
        self.assertIsNone(result)

    def test_populate_procedure_button_text(self):
        populate_procedure_button_text()
        registry = getUtility(IRegistry)
        labels = registry.get("smartweb.procedure_button_text")
        self.assertIsNotNone(labels)
        self.assertGreater(len(labels), 0)
