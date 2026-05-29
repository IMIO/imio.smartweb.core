# -*- coding: utf-8 -*-
# Post-migration fix: reindex `related_quickaccess` on folders.
#
# Why this exists
# ---------------
# `@@import_relations` (collective.exportimport.import_other.ImportRelations)
# délègue à `Products.CMFPlone.relationhelper.restore_relations` (Plone 6).
# Cette fonction repose les valeurs via `setattr(source_obj, field, …)` puis
# appelle uniquement `updateRelations()` + `update_behavior_relations()` pour
# rafraîchir le catalog zc.relation. Elle ne déclenche jamais
# `notify(ObjectModifiedEvent)` ni `obj.reindexObject()`.
#
# Or l'index/metadata `related_quickaccess` (imio.smartweb.core.indexers
# l. 104-108 ; profiles/default/catalog.xml : FieldIndex + column) vit dans le
# `portal_catalog`, pas dans le catalog des relations. Et la viewlet de
# navigation (viewlets/navigation.py:99-102) lit la valeur depuis le brain
# (`brain.related_quickaccess`), pas depuis l'objet.
#
# Conséquence : après @@import_content + @@import_relations, les RelationList
# `quick_access_items` sont bien posées sur les Folders, mais l'index/metadata
# restent vides jusqu'à un reindex du folder. C'est pour ça qu'un Edit→Save
# manuel suffit à faire apparaître les accès rapides dans la nav (le save
# déclenche ObjectModifiedEvent → reindexObject complet).
#
# Cette vue, à appeler une fois après @@import_relations, itère les
# `imio.smartweb.Folder` ayant un `quick_access_items` non-vide et réindexe
# l'index `related_quickaccess` (qui met aussi à jour la colonne metadata du
# même nom — Plone réindexe metadata même quand `idxs=[…]` est passé).
#
# Note : `obj.reindexObject(idxs=[…])` met à jour à la fois l'index ET la
# colonne metadata (CMFCatalogAware.reindexObject → catalog_object avec
# update_metadata=1 par défaut), donc pas besoin d'un reindex complet.

from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five.browser import BrowserView
from zope.interface import alsoProvides

import logging
import transaction


logger = logging.getLogger(__name__)

COMMIT_EVERY = 500


class ReindexQuickaccessView(BrowserView):

    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        reindexed = 0
        skipped = 0
        errors = 0
        for brain in api.content.find(portal_type="imio.smartweb.Folder"):
            try:
                obj = brain.getObject()
            except Exception:
                logger.warning(
                    "imio.smartweb.core : reindex_quickaccess — "
                    "cannot wake object at %s",
                    brain.getPath(),
                )
                errors += 1
                continue
            qa = getattr(obj, "quick_access_items", None)
            if not qa:
                skipped += 1
                continue
            obj.reindexObject(idxs=["related_quickaccess"])
            reindexed += 1
            if reindexed % COMMIT_EVERY == 0:
                transaction.commit()
                logger.info(
                    "imio.smartweb.core : reindex_quickaccess — "
                    "%s folders reindexed (intermediate commit)",
                    reindexed,
                )
        # Commit explicite : indispensable en bin/instance debug, sans effet
        # de bord en HTTP (Zope commit déjà en fin de requête).
        transaction.commit()
        msg = (
            "imio.smartweb.core : reindex_quickaccess — "
            "reindexed {} folder(s), skipped {} (no quick_access_items), "
            "{} error(s)"
        ).format(reindexed, skipped, errors)
        logger.info(msg)
        return msg
