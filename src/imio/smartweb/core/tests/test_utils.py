# -*- coding: utf-8 -*-

from collective.taxonomy.interfaces import ITaxonomy
from freezegun import freeze_time
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import clear_ram_cache
from imio.smartweb.core.tests.utils import make_named_image
from imio.smartweb.core.tests.utils import rename_term
from imio.smartweb.core.utils import all_term_labels
from imio.smartweb.core.utils import batch_results
from imio.smartweb.core.utils import changed_terms
from imio.smartweb.core.utils import get_plausible_vars
from imio.smartweb.core.utils import get_scale_url
from imio.smartweb.core.utils import get_ts_api_url
from imio.smartweb.core.utils import is_valid_url
from imio.smartweb.core.utils import populate_procedure_button_text
from imio.smartweb.core.utils import reindex_searchable_text
from imio.smartweb.core.utils import reindexing_changed_terms
from imio.smartweb.core.utils import remove_cache_key
from imio.smartweb.core.utils import taxonomy_fields
from imio.smartweb.core.utils import term_labels
from imio.smartweb.core.tests.utils import get_json
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.namedfile.file import NamedBlobImage
from plone.registry.interfaces import IRegistry
from plone.uuid.interfaces import IUUID
from Products.CMFCore.indexing import processQueue
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


class TestTaxonomyUtils(ImioSmartwebTestCase):
    """Taxonomy helpers of utils.py"""

    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.utility = getUtility(ITaxonomy, name="collective.taxonomy.page_category")
        self.page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="My page",
            language="fr",
        )
        self.page.taxonomy_page_category = ["emploi"]
        self.page.reindexObject()
        # index now, not at the first search, which comes after a renaming
        processQueue()

    def tearDown(self):
        clear_ram_cache()

    def find(self, text):
        return [b.getObject() for b in api.content.find(SearchableText=text)]

    def test_taxonomy_fields(self):
        fields = dict(taxonomy_fields())
        self.assertEqual(fields["taxonomy_page_category"], self.utility)
        self.assertIn("taxonomy_procedure_category", fields)

    def test_term_labels(self):
        labels = term_labels(self.utility, "fr")
        self.assertEqual(labels["emploi"], "Emploi")
        self.assertEqual(term_labels(self.utility, "nl")["emploi"], "Werk")
        # a language the taxonomy does not have falls back on another one
        self.assertIn("emploi", term_labels(self.utility, "xx"))
        # the stored data gives the new label at once, in the same transaction
        rename_term("emploi", "Emploi et formation")
        self.assertEqual(
            term_labels(self.utility, "fr")["emploi"], "Emploi et formation"
        )

    def test_all_term_labels(self):
        labels = all_term_labels()
        self.assertEqual(labels["taxonomy_page_category"]["fr"]["emploi"], "Emploi")
        self.assertEqual(labels["taxonomy_page_category"]["en"]["emploi"], "Job")

    def test_changed_terms(self):
        before = {"taxonomy_a": {"fr": {"x": "X", "y": "Y", "z": "Z"}}}
        after = {"taxonomy_a": {"fr": {"x": "X", "y": "Y2"}}}
        # renamed and removed terms change, the others do not
        self.assertEqual(changed_terms(before, after), {"taxonomy_a": {"y", "z"}})
        self.assertEqual(changed_terms(before, before), {})
        # a change in one language is enough
        after = {"taxonomy_a": {"fr": before["taxonomy_a"]["fr"], "nl": {"x": "X"}}}
        self.assertEqual(changed_terms(before, after), {"taxonomy_a": {"x"}})

    def test_reindex_searchable_text(self):
        rename_term("emploi", "Recrutement")
        self.assertEqual(self.find("Recrutement"), [])
        reindex_searchable_text("taxonomy_page_category", {"emploi"})
        self.assertEqual(self.find("Recrutement"), [self.page])

    def test_reindexing_changed_terms(self):
        with reindexing_changed_terms():
            rename_term("emploi", "Recrutement")
        self.assertEqual(self.find("Recrutement"), [self.page])
        self.assertEqual(self.find("Emploi"), [])
