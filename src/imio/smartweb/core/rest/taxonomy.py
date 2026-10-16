# -*- coding: utf-8 -*-

from collective.taxonomy.restapi.services.taxonomy.update import TaxonomyPatch
from imio.smartweb.core.utils import reindexing_changed_terms


class SmartwebTaxonomyPatch(TaxonomyPatch):
    """Patch a taxonomy, then reindex the objects whose term labels changed
    (see indexers.SmartwebIndexableObjectWrapper)."""

    def reply(self):
        with reindexing_changed_terms():
            return super().reply()
