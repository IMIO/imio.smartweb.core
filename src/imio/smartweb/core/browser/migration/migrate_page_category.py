# -*- coding: utf-8 -*-

from collective.instancebehavior import instance_behaviors_of
from collective.taxonomy.interfaces import ITaxonomy
from imio.smartweb.core.browser.migration.taxonomy_mapping import AVISENQUETES_FIELD
from imio.smartweb.core.browser.migration.taxonomy_mapping import AVISENQUETES_ROOT_TERM
from imio.smartweb.core.browser.migration.taxonomy_mapping import AVISENQUETES_TAXONOMY
from imio.smartweb.core.browser.migration.taxonomy_mapping import PAGE_CATEGORY_FIELD
from imio.smartweb.core.browser.migration.taxonomy_mapping import (
    PAGE_CATEGORY_TO_AVISENQUETES,
)
from imio.smartweb.core.browser.migration.taxonomy_mapping import (
    PAGE_CATEGORY_TO_REGLEMENTS,
)
from imio.smartweb.core.browser.migration.taxonomy_mapping import REGLEMENTS_FIELD
from imio.smartweb.core.browser.migration.taxonomy_mapping import REGLEMENTS_ROOT_TERM
from imio.smartweb.core.browser.migration.taxonomy_mapping import REGLEMENTS_TAXONOMY
from plone import api
from plone.behavior.interfaces import IBehavior
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five.browser import BrowserView
from zope.interface import alsoProvides

import logging

logger = logging.getLogger("imio.smartweb.core")

# The Liège site created sub terms under the "avis_et_enquete" and "reglement"
# root terms of page_category. Those terms now live in their own taxonomies, so
# this one shot view moves the value of every page to the right taxonomy and
# falls back on the matching root term for page_category (that field is single
# select, emptying it would drop the page out of the navigation listings).
#
# Run it once on the Liège instance, as a Manager:
#   /Plone/@@migrate_page_category            -> dry run, changes nothing
#   /Plone/@@migrate_page_category?apply=1    -> actually migrates

MIGRATIONS = (
    (
        AVISENQUETES_TAXONOMY,
        AVISENQUETES_FIELD,
        AVISENQUETES_ROOT_TERM,
        PAGE_CATEGORY_TO_AVISENQUETES,
    ),
    (
        REGLEMENTS_TAXONOMY,
        REGLEMENTS_FIELD,
        REGLEMENTS_ROOT_TERM,
        PAGE_CATEGORY_TO_REGLEMENTS,
    ),
)


class MigratePageCategoryView(BrowserView):

    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        self.apply = self.request.form.get("apply") in ("1", "true", "True")
        self.errors = self.check_prerequisites()
        self.migrated = []
        self.kept = []
        self.stale = []
        self.not_enabled = []
        if self.errors:
            return self.index()

        sm = api.portal.get().getSiteManager()
        single_select = {}
        generated_names = {}
        for taxonomy_name, field, _root, _mapping in MIGRATIONS:
            taxonomy = sm.queryUtility(ITaxonomy, name=taxonomy_name)
            generated_names[field] = taxonomy.getGeneratedName()
            single_select[field] = self.is_single_select(taxonomy_name)
        fti_behaviors = api.portal.get_tool("portal_types")[
            "imio.smartweb.Page"
        ].behaviors
        for brain in api.content.find(portal_type="imio.smartweb.Page"):
            try:
                obj = brain.getObject()
            except (AttributeError, KeyError):
                # Stale catalog entry: the object behind it is gone. Report the
                # path instead of blowing up in the middle of the migration.
                self.stale.append(brain.getPath())
                continue
            old_term = getattr(obj.aq_base, PAGE_CATEGORY_FIELD, None)
            if not old_term:
                continue
            for _taxonomy_name, field, root_term, mapping in MIGRATIONS:
                if old_term not in mapping:
                    continue
                new_term = mapping[old_term]
                row = {
                    "path": brain.getPath(),
                    "title": brain.Title,
                    "old_term": old_term,
                    "field": field,
                    "new_term": new_term,
                    "root_term": root_term,
                }
                # The behavior can be on the content type or turned on object by
                # object with the "Taxonomies choices" form. Without either, the
                # field would not be readable, so report instead of writing.
                if generated_names[field] not in fti_behaviors and generated_names[
                    field
                ] not in instance_behaviors_of(obj):
                    self.not_enabled.append(row)
                    break
                # A value entered by an editor always wins over the migrated one.
                if getattr(obj.aq_base, field, None):
                    self.kept.append(row)
                else:
                    self.migrated.append(row)
                if self.apply:
                    if not getattr(obj.aq_base, field, None):
                        setattr(
                            obj,
                            field,
                            new_term if single_select[field] else [new_term],
                        )
                    setattr(obj, PAGE_CATEGORY_FIELD, root_term)
                    obj.reindexObject(idxs=self.indexes_to_update())
                break

        if self.not_enabled:
            logger.warning(
                "migrate_page_category: {} page(s) skipped, the target taxonomy "
                "behavior is enabled neither on imio.smartweb.Page nor on the "
                "page itself".format(len(self.not_enabled))
            )
        if self.stale:
            logger.warning(
                "migrate_page_category: {} stale catalog entrie(s) skipped: "
                "{}".format(len(self.stale), ", ".join(self.stale))
            )
        if self.apply:
            logger.info(
                "migrate_page_category: {} page(s) migrated, {} page(s) already "
                "had a term in the target taxonomy and kept it".format(
                    len(self.migrated), len(self.kept)
                )
            )
        return self.index()

    def check_prerequisites(self):
        """Both taxonomies must exist, with their behavior registered.

        Where the behavior is *enabled* is not checked here: it can be on the
        imio.smartweb.Page content type or turned on object by object with the
        "Taxonomies choices" form, so it is decided per page.
        """
        errors = []
        sm = api.portal.get().getSiteManager()
        for taxonomy_name, _field, _root, _mapping in MIGRATIONS:
            taxonomy = sm.queryUtility(ITaxonomy, name=taxonomy_name)
            if taxonomy is None:
                errors.append(
                    "La taxonomie {} n'existe pas sur ce site.".format(taxonomy_name)
                )
            elif sm.queryUtility(IBehavior, name=taxonomy.getGeneratedName()) is None:
                errors.append(
                    "La taxonomie {} n'a pas de comportement enregistré.".format(
                        taxonomy_name
                    )
                )
        return errors

    def is_single_select(self, taxonomy_name):
        """True when the generated behavior stores a single value, not a list."""
        sm = api.portal.get().getSiteManager()
        taxonomy = sm.queryUtility(ITaxonomy, name=taxonomy_name)
        behavior = sm.queryUtility(IBehavior, name=taxonomy.getGeneratedName())
        return bool(getattr(behavior, "is_single_select", True))

    def indexes_to_update(self):
        catalog = api.portal.get_tool("portal_catalog")
        return [
            idx
            for idx in (
                PAGE_CATEGORY_FIELD,
                AVISENQUETES_FIELD,
                REGLEMENTS_FIELD,
                "category_and_topics",
            )
            if idx in catalog.indexes()
        ]
