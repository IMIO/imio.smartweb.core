# -*- coding: utf-8 -*-

from collections import Counter
from collective.solr.interfaces import ISearch
from collective.solr.utils import isActive
from collective.taxonomy.interfaces import ITaxonomy
from eea.facetednavigation.interfaces import IFacetedCatalog
from eea.facetednavigation.search.catalog import FacetedCatalog
from plone import api
from plone.behavior.interfaces import IBehavior
from zope.component import queryUtility
from zope.component.hooks import getSite
from zope.interface import implementer

import logging

logger = logging.getLogger("imio.smartweb.core")

# Filtering on a taxonomy Solr ignores means pulling the result set into memory.
# Past this many documents the trade stops being worth it: we keep the first
# ones and say so in the log rather than put the instance at risk.
MAX_LOCAL_FILTER_RESULTS = 5000


def taxonomy_index_names():
    """Catalog index name of every collective.taxonomy taxonomy.

    Names are rebuilt the way collective.taxonomy builds them itself (see
    collective/taxonomy/collectionfilter.py), so a taxonomy created through the
    web is covered without a hardcoded list that would drift.
    """
    site = getSite()
    if site is None:
        return set()
    sm = site.getSiteManager()
    names = set()
    for _name, utility in sm.getUtilitiesFor(ITaxonomy):
        behavior = sm.queryUtility(IBehavior, name=utility.getGeneratedName())
        if behavior is None:
            continue
        prefix = getattr(behavior, "field_prefix", "") or ""
        names.add("{0}{1}".format(prefix, utility.getShortName()))
    return names


def solr_schema():
    """Solr schema of the default core, or None when Solr cannot be read"""
    search = queryUtility(ISearch)
    if search is None:
        return None
    try:
        return search.getManager().getSchema()
    except Exception:  # noqa - solr down, inactive or misconfigured
        logger.warning("Could not read the Solr schema", exc_info=True)
        return None


def matches_solr_requirements(query, required):
    """Whether `query` carries what collective.solr demands to take the query.

    Pure counterpart of the dispatch decision in
    collective/solr/dispatcher.py:75-84.
    """
    if query.get("use_solr", False):
        return True
    if not required:
        return True
    present = set(required).intersection(query)
    if not present:
        return False
    return all(query[key] for key in present)


def uses_solr(query):
    """Whether Solr will answer `query`, or the portal catalog will.

    This matters more than it looks: `collective.solr.required` is
    ``SearchableText`` by default, so a faceted query made of a taxonomy
    criterion alone never reaches Solr - the portal catalog answers it, and the
    portal catalog knows every taxonomy index, TTW ones included. Selecting a
    value in an unknown taxonomy has therefore always worked; only mixing it
    with a text search ever reached Solr and broke. We must stay out of the way
    of the path that already works.
    """
    if not isActive():
        return False
    required = api.portal.get_registry_record("collective.solr.required", default=None)
    return matches_solr_requirements(query, required)


def unindexed_taxonomies(query, schema, taxonomy_names):
    """Taxonomy criteria of `query` that are missing from the Solr schema.

    Solr answers 400 ("undefined field") as soon as such an index is used as a
    facet, and eea turns that into an empty batch, so the visitor gets no
    results at all instead of an error.
    """
    if not schema:
        return {}
    return {
        name: value
        for name, value in query.items()
        if name in taxonomy_names and schema.get(name) is None
    }


def unindexed_criteria(query):
    """Criteria of `query` that would make Solr reject the whole request.

    Empty when the portal catalog is going to answer anyway: it needs no help
    and filters the taxonomy natively.
    """
    if not uses_solr(query):
        return {}
    return unindexed_taxonomies(query, solr_schema(), taxonomy_index_names())


def strip_criteria(query, criteria):
    """Remove `criteria` from `query` in place, as filters and as facets"""
    for name in criteria:
        query.pop(name, None)
    facet_fields = [
        name for name in query.get("facet.field") or [] if name not in criteria
    ]
    if facet_fields:
        query["facet.field"] = facet_fields
    else:
        # collective.solr drops "facet=true" on its own once no field is left
        query.pop("facet.field", None)
    return query


def as_tuple(value):
    """Normalize a catalog value to a tuple, without exploding strings"""
    if not value:
        return ()
    if isinstance(value, str):
        return (value,)
    return tuple(value)


def filter_and_count(brains, values_by_uid, criteria):
    """Apply `criteria` to `brains`, and count values over the unfiltered set.

    Counting before filtering is what a facet is meant to show: how many results
    each value would yield.
    """
    wanted = {name: set(as_tuple(value)) for name, value in criteria.items()}
    counts = {name: Counter() for name in criteria}
    filtered = []
    for brain in brains:
        values = values_by_uid.get(brain["UID"], {})
        for name in criteria:
            counts[name].update(values.get(name, ()))
        if all(wanted[name] & set(values.get(name, ())) for name in criteria):
            filtered.append(brain)
    return filtered, counts


class FilteredResults(list):
    """Filtered brains that keep the facet counts a plain list would lose.

    eea only reads facet counts off a result set that exposes ``facet_counts``
    (eea/facetednavigation/widgets/widget.py:329-332); without it every countable
    widget on the page would silently lose its numbers.
    """

    def __init__(self, brains, facet_counts):
        super(FilteredResults, self).__init__(brains)
        self.facet_counts = facet_counts


@implementer(IFacetedCatalog)
class SmartwebFacetedCatalog(FacetedCatalog):
    """Faceted catalog that survives taxonomies Solr does not know.

    A taxonomy created through the web gets a catalog index that is absent from
    the shared Solr schema, and that schema cannot be extended per client. eea
    adds the index to ``facet.field`` without checking it
    (eea/facetednavigation/browser/app/query.py:93-98) and collective.solr
    forwards facet parameters verbatim (collective/solr/mangler.py:275-276), so
    Solr rejects the whole request with a 400 and the page comes back empty.

    Such criteria are therefore removed from the Solr query and applied here on
    the results instead, with their facet counts rebuilt from the catalog
    metadata column collective.taxonomy maintains.

    Only queries Solr actually answers are touched: a taxonomy criterion on its
    own falls back to the portal catalog, which handles it natively, and is left
    strictly alone. See ``uses_solr``.
    """

    def __call__(self, context, **query):
        criteria = unindexed_criteria(query)
        if not criteria:
            return super(SmartwebFacetedCatalog, self).__call__(context, **query)

        logger.warning(
            "Taxonomy index(es) %s unknown to the Solr schema, filtering them "
            "in memory on %s (at most %s documents)",
            ", ".join(sorted(criteria)),
            context.absolute_url(),
            MAX_LOCAL_FILTER_RESULTS,
        )
        brains = super(SmartwebFacetedCatalog, self).__call__(
            context, **self.solr_query(query, criteria)
        )
        values = self.taxonomy_values(brains, criteria)
        filtered, counts = filter_and_count(brains, values, criteria)
        return FilteredResults(filtered, self.merge_counts(brains, counts))

    @staticmethod
    def solr_query(query, criteria):
        """The query Solr can answer: no unknown index, no server side batch.

        Batching has to go as well: `criteria` are applied after the search, so
        a page computed by Solr would be the wrong page.
        """
        query = strip_criteria(dict(query), criteria)
        query.pop("b_start", None)
        query["b_size"] = MAX_LOCAL_FILTER_RESULTS
        return query

    @staticmethod
    def taxonomy_values(brains, criteria):
        """Taxonomy values of the results, read from the catalog metadata.

        collective.taxonomy keeps a metadata column per taxonomy
        (collective/taxonomy/behavior.py:164-167), so a single catalog query on
        the UIDs Solr returned is enough - no object gets woken up.
        """
        uids = [brain["UID"] for brain in brains if brain.get("UID")]
        if not uids:
            return {}
        catalog = api.portal.get_tool("portal_catalog")
        # the monkey patched searchResults would send us straight back to Solr
        search = getattr(catalog, "_cs_old_searchResults", catalog.searchResults)
        return {
            brain.UID: {name: as_tuple(getattr(brain, name, None)) for name in criteria}
            for brain in search(UID=uids)
        }

    @staticmethod
    def merge_counts(brains, counts):
        """Facet counts returned by Solr, completed with the ones we computed"""
        facet_counts = dict(getattr(brains, "facet_counts", None) or {})
        facet_fields = dict(facet_counts.get("facet_fields") or {})
        for name, counter in counts.items():
            facet_fields[name] = dict(counter)
        facet_counts["facet_fields"] = facet_fields
        return facet_counts


def strip_unindexed_taxonomies(event):
    """Last resort guard on the final faceted query.

    SmartwebFacetedCatalog handles the criteria coming from faceted widgets, but
    a Collection stored query can carry the same index and is merged in later
    (eea/facetednavigation/search/catalog.py:68-81). Dropping it here keeps Solr
    from rejecting the whole request; the criterion is then not applied at all,
    which still beats an empty page.
    """
    query = event.query
    criteria = unindexed_criteria(query)
    if not criteria:
        return
    logger.warning(
        "Taxonomy index(es) %s unknown to the Solr schema, dropped from the "
        "query on %s",
        ", ".join(sorted(criteria)),
        event.object.absolute_url(),
    )
    strip_criteria(query, criteria)
