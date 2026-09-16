# -*- coding: utf-8 -*-

from eea.facetednavigation.interfaces import IFacetedCatalog
from imio.smartweb.core.faceted.catalog import as_tuple
from imio.smartweb.core.faceted.catalog import filter_and_count
from imio.smartweb.core.faceted.catalog import FilteredResults
from imio.smartweb.core.faceted.catalog import MAX_LOCAL_FILTER_RESULTS
from imio.smartweb.core.faceted.catalog import matches_solr_requirements
from imio.smartweb.core.faceted.catalog import SmartwebFacetedCatalog
from imio.smartweb.core.faceted.catalog import solr_schema
from imio.smartweb.core.faceted.catalog import strip_criteria
from imio.smartweb.core.faceted.catalog import taxonomy_index_names
from imio.smartweb.core.faceted.catalog import unindexed_criteria
from imio.smartweb.core.faceted.catalog import unindexed_taxonomies
from imio.smartweb.core.faceted.catalog import uses_solr
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.uuid.interfaces import IUUID
from zope.component import getUtility

# A Solr schema is a dict-like object collective.solr only ever reads with
# .get(), so the shipped "web" core is described here by the field names that
# matter. The taxonomy created TTW is deliberately absent.
SOLR_SCHEMA = {
    "SearchableText": object(),
    "Title": object(),
    "portal_type": object(),
    "taxonomy_page_category": object(),
}


class TestCatalog(ImioSmartwebTestCase):
    """Module level helpers of faceted/catalog.py"""

    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_taxonomy_index_names(self):
        names = taxonomy_index_names()
        self.assertIn("taxonomy_page_category", names)
        self.assertIn("taxonomy_procedure_category", names)
        # only taxonomies, not every catalog index
        self.assertNotIn("SearchableText", names)
        self.assertNotIn("portal_type", names)

    def test_solr_schema(self):
        # no Solr connection in the test environment: callers must cope with it
        # instead of blowing up
        self.assertIsNone(solr_schema())

    def test_unindexed_taxonomies(self):
        names = {"taxonomy_page_category", "taxonomy_reglements"}
        query = {
            "SearchableText": "taxe",
            "portal_type": ["imio.smartweb.Page"],
            "taxonomy_page_category": "known",
            "taxonomy_reglements": "cc82v8yhd1",
        }
        self.assertEqual(
            unindexed_taxonomies(query, SOLR_SCHEMA, names),
            {"taxonomy_reglements": "cc82v8yhd1"},
        )

        # a taxonomy Solr knows is left alone
        self.assertEqual(
            unindexed_taxonomies(
                {"taxonomy_page_category": "known"}, SOLR_SCHEMA, names
            ),
            {},
        )

        # an unknown index that is not a taxonomy is none of our business:
        # collective.solr drops it from the query on its own
        self.assertEqual(
            unindexed_taxonomies({"use_solr": True, "core": "web"}, SOLR_SCHEMA, names),
            {},
        )

        # no schema (Solr down) means no decision can be made, so touch nothing
        self.assertEqual(
            unindexed_taxonomies({"taxonomy_reglements": "x"}, None, names), {}
        )

    def test_matches_solr_requirements(self):
        # SearchableText is what collective.solr ships as required, so a
        # taxonomy criterion on its own never reaches Solr
        required = ["SearchableText"]
        self.assertFalse(
            matches_solr_requirements({"taxonomy_reglements": "x"}, required)
        )
        self.assertTrue(
            matches_solr_requirements(
                {"SearchableText": "taxe", "taxonomy_reglements": "x"}, required
            )
        )
        # present but empty: collective.solr falls back too
        self.assertFalse(matches_solr_requirements({"SearchableText": ""}, required))
        # forced by the caller, whatever else the query holds
        self.assertTrue(matches_solr_requirements({"use_solr": True}, required))
        # nothing required: everything goes to Solr
        self.assertTrue(matches_solr_requirements({"anything": 1}, []))

    def test_uses_solr(self):
        # Solr is inactive in the test environment, so nothing is dispatched to
        # it and the portal catalog answers every query
        self.assertFalse(uses_solr({"SearchableText": "taxe"}))

    def test_unindexed_criteria(self):
        # Solr inactive: the portal catalog knows the taxonomy index, so there
        # is nothing to work around
        self.assertEqual(unindexed_criteria({"taxonomy_page_category": "x"}), {})

    def test_strip_criteria(self):
        query = {
            "SearchableText": "taxe",
            "taxonomy_reglements": "cc82v8yhd1",
            "facet.field": [
                "topics",
                "taxonomy_page_category",
                "taxonomy_reglements",
            ],
        }
        strip_criteria(query, {"taxonomy_reglements": "cc82v8yhd1"})
        self.assertEqual(
            query,
            {
                "SearchableText": "taxe",
                "facet.field": ["topics", "taxonomy_page_category"],
            },
        )

        # the last facet field going away takes the key with it, so that
        # collective.solr stops sending facet=true
        query = {"facet.field": ["taxonomy_reglements"], "taxonomy_reglements": "x"}
        strip_criteria(query, {"taxonomy_reglements": "x"})
        self.assertEqual(query, {})

    def test_as_tuple(self):
        self.assertEqual(as_tuple(["a", "b"]), ("a", "b"))
        # a single select taxonomy stores a string: it must stay one value,
        # not be exploded into characters
        self.assertEqual(as_tuple("abc"), ("abc",))
        self.assertEqual(as_tuple(None), ())
        self.assertEqual(as_tuple(""), ())

    def test_filter_and_count(self):
        brains = [{"UID": "uid1"}, {"UID": "uid2"}, {"UID": "uid3"}]
        values = {
            "uid1": {"taxonomy_reglements": ("taxes",)},
            "uid2": {"taxonomy_reglements": ("taxes", "urbanisme")},
            "uid3": {"taxonomy_reglements": ("urbanisme",)},
        }
        filtered, counts = filter_and_count(
            brains, values, {"taxonomy_reglements": "taxes"}
        )
        self.assertEqual([b["UID"] for b in filtered], ["uid1", "uid2"])
        # counts cover the whole result set, not the filtered one: that is what
        # a facet shows
        self.assertEqual(counts["taxonomy_reglements"], {"taxes": 2, "urbanisme": 2})

        # a result carrying no value for the taxonomy is simply filtered out
        filtered, counts = filter_and_count(
            brains + [{"UID": "uid4"}], values, {"taxonomy_reglements": "taxes"}
        )
        self.assertEqual([b["UID"] for b in filtered], ["uid1", "uid2"])

    def test_filtered_results(self):
        results = FilteredResults([{"UID": "uid1"}], {"facet_fields": {"a": {"b": 1}}})
        self.assertEqual(len(results), 1)
        self.assertEqual(results.facet_counts, {"facet_fields": {"a": {"b": 1}}})
        # a plain list would make eea fall back to its ZCatalog counting branch,
        # which cannot work on Solr flares
        self.assertTrue(hasattr(results, "facet_counts"))


class TestSmartwebFacetedCatalog(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.collection = api.content.create(
            container=self.portal,
            type="Collection",
            title="A collection",
        )

    def test_utility_is_ours(self):
        self.assertIsInstance(getUtility(IFacetedCatalog), SmartwebFacetedCatalog)

    def test_call_without_unindexed_taxonomy(self):
        # nothing to work around: results come back as usual, and the batch
        # keys stay in the query so Solr can paginate server side
        for i in range(3):
            api.content.create(
                container=self.portal,
                type="imio.smartweb.Page",
                title="Page {0}".format(i),
            )
        catalog = getUtility(IFacetedCatalog)
        brains = catalog(self.collection, portal_type="imio.smartweb.Page")
        self.assertEqual(len(brains), 3)
        self.assertNotIsInstance(brains, FilteredResults)

    def test_call_with_taxonomy_only_still_filters(self):
        """A taxonomy criterion on its own has always worked and must keep
        working: the query never reaches Solr, the portal catalog answers it and
        filters on the taxonomy index natively."""
        page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="Avis d'enquete",
        )
        page.taxonomy_page_category = ["avis_et_enquete"]
        page.reindexObject()
        api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="Sans categorie",
        )

        catalog = getUtility(IFacetedCatalog)
        brains = catalog(
            self.collection,
            portal_type="imio.smartweb.Page",
            taxonomy_page_category="avis_et_enquete",
        )
        self.assertEqual([brain.Title for brain in brains], ["Avis d'enquete"])

    def test_solr_query(self):
        query = {
            "SearchableText": "taxe",
            "taxonomy_reglements": "cc82v8yhd1",
            "facet.field": ["topics", "taxonomy_reglements"],
            "b_start": 20,
            "b_size": 10,
        }
        self.assertEqual(
            SmartwebFacetedCatalog.solr_query(
                query, {"taxonomy_reglements": "cc82v8yhd1"}
            ),
            {
                "SearchableText": "taxe",
                "facet.field": ["topics"],
                "b_size": MAX_LOCAL_FILTER_RESULTS,
            },
        )
        # the caller's query is left untouched
        self.assertEqual(query["b_start"], 20)
        self.assertIn("taxonomy_reglements", query)

    def test_taxonomy_values(self):
        page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="Taxe de stationnement",
        )
        # a real identifier of the shipped page_category taxonomy: the indexer
        # silently drops anything the taxonomy does not know
        page.taxonomy_page_category = ["avis_et_enquete"]
        page.reindexObject()
        uid = IUUID(page)

        values = SmartwebFacetedCatalog.taxonomy_values(
            [{"UID": uid}], {"taxonomy_page_category": "avis_et_enquete"}
        )
        self.assertEqual(
            values, {uid: {"taxonomy_page_category": ("avis_et_enquete",)}}
        )

        # a result with no value for that taxonomy still gets an entry
        other = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="Sans categorie",
        )
        values = SmartwebFacetedCatalog.taxonomy_values(
            [{"UID": IUUID(other)}], {"taxonomy_page_category": "avis_et_enquete"}
        )
        self.assertEqual(values, {IUUID(other): {"taxonomy_page_category": ()}})

        self.assertEqual(SmartwebFacetedCatalog.taxonomy_values([], {}), {})

    def test_merge_counts(self):
        class SolrBrains(list):
            facet_counts = {"facet_fields": {"topics": {"economics": 4}}}

        merged = SmartwebFacetedCatalog.merge_counts(
            SolrBrains(), {"taxonomy_reglements": {"taxes": 2}}
        )
        self.assertEqual(
            merged["facet_fields"],
            {"topics": {"economics": 4}, "taxonomy_reglements": {"taxes": 2}},
        )

        # no faceting was asked of Solr: our counts are all there is
        merged = SmartwebFacetedCatalog.merge_counts(
            [], {"taxonomy_reglements": {"taxes": 2}}
        )
        self.assertEqual(
            merged, {"facet_fields": {"taxonomy_reglements": {"taxes": 2}}}
        )


# <audit>
#   <file>test_faceted_catalog.py</file>
#   <requirements_applied>R1, R4, R5, R6</requirements_applied>
#   <deviations>
#     R1: SOLR_SCHEMA is a plain dict rather than a live Solr schema. It is not a
#     mock of a Plone internal - collective.solr only ever reads the schema with
#     .get(), so a dict is the real contract - but the test environment has no
#     Solr, so the Solr side of the integration is described, not exercised.
#     R2: most tests here drive module level functions directly instead of
#     create content -> act -> observe. The user visible workflow (a faceted
#     search on a TTW taxonomy returning results instead of an empty page)
#     cannot be reproduced without a running Solr; the workflow style is used
#     where it does work (test_call_without_unindexed_taxonomy,
#     test_taxonomy_values).
#   </deviations>
#   <questions>
#     Should a Solr backed functional test be added to cover the filtering path
#     end to end? It would need a Solr instance in CI, which no existing test
#     requires today.
#   </questions>
# </audit>
