# -*- coding: utf-8 -*-
# Repair view: re-clone Image blobs that were posted empty.
#
# Why this exists
# ---------------
# Une version précédente de `_copy_blob_from_canonical` (dans import_content.py)
# faisait `obj.image = copy.deepcopy(source_image)`. `copy.deepcopy` sur un
# `NamedBlobImage` crée bien un nouveau `Blob` ZODB, mais ne recopie pas les
# données binaires du fichier blob sous-jacent (Blob est un Persistent et son
# __deepcopy__ ne lit pas le payload). Résultat : tous les clones créés avec
# l'ancien code ont un fichier .blob de 0 octet sur disque, et PIL lève
# `UnidentifiedImageError` au scaling → vignettes cassées en front.
#
# Cette vue parcourt `_OUTPUT_CONTENTS.json`, retrouve chaque item porteur de
# `_clone_blob_from`, le localise dans Plone par son chemin `@id`, vérifie si
# son blob image est vide (taille 0 ou attribut absent) et, si oui, le
# reconstitue depuis l'image canonique via le bon pattern :
#     NamedBlobImage(data=source.image.data, filename=..., contentType=...)
# qui force la lecture des octets et l'écriture d'un nouveau blob non vide.
#
# Usage
# -----
# Démarrer Plone APRÈS avoir rechargé le code (fix dans import_content.py),
# puis appeler :
#     @@reclone_empty_blobs?jsonfile=/abs/path/to/_OUTPUT_CONTENTS.json
#         [&blob_home=/abs/path/to/blobstorage_liege]
#         [&dry_run=1]
#
# `blob_home` est le blobstorage du *site source* (le CPSkin exporté). Si
# fourni, la vue lit le blob du canonical directement depuis l'export quand
# elle ne retrouve pas l'item canonical en Plone (cas des imports successifs
# qui ont aplati la hiérarchie : le @id JSON ne correspond plus au chemin
# réel de l'objet en Plone). Si l'objet canonical est trouvable en Plone, on
# privilégie cette voie (le blob y est validé). Sinon → fallback fichier.

from plone import api
from plone.namedfile.file import NamedBlobImage
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five.browser import BrowserView
from urllib.parse import urlparse
from zope.interface import alsoProvides

import json
import logging
import os
import transaction

logger = logging.getLogger(__name__)

COMMIT_EVERY = 200


class RecloneEmptyBlobsView(BrowserView):
    def _relpath_from_atid(self, atid):
        """`http://host/Plone/foo/bar` → `foo/bar` (sans l'id du portail)."""
        if not atid:
            return None
        parts = [p for p in urlparse(atid).path.split("/") if p]
        if not parts:
            return None
        portal_id = api.portal.get().getId()
        if parts[0] == portal_id:
            parts = parts[1:]
        return "/".join(parts)

    def _traverse(self, portal, relpath):
        if not relpath:
            return None
        try:
            return portal.unrestrictedTraverse(relpath)
        except Exception:
            return None

    def _blob_size(self, image_field):
        """Retourne la taille RÉELLE du fichier blob sur disque.

        On n'utilise PAS `image_field.getSize()` qui retourne la valeur mise
        en cache dans `__dict__["size"]` (c'est précisément ce cache que
        l'ancien `copy.deepcopy(NamedBlobImage)` a copié depuis la source).
        Stratégie :
          1) `blob.committed()` → chemin sur disque → `os.path.getsize` :
             c'est la voie la plus directe, qui contourne tout buffer Python.
          2) fallback : `blob.open("r") + seek(0,2) + tell()`.
        """
        if image_field is None:
            return 0
        blob = getattr(image_field, "_blob", None)
        if blob is None:
            return 0
        try:
            path = blob.committed()
        except Exception:
            path = None
        if path and os.path.exists(path):
            return os.path.getsize(path)
        try:
            with blob.open("r") as fp:
                fp.seek(0, 2)
                return fp.tell()
        except Exception:
            return 0

    def _read_source_from_export(self, canonical_item, blob_home):
        """Lit les octets de l'image canonique directement depuis l'export
        CPSkin (`blobstorage_liege`/…). Retourne (data, filename, contentType,
        size) ou (None, None, None, 0) si non disponible.
        """
        if not blob_home:
            return None, None, None, 0
        img = canonical_item.get("image") or {}
        rel_blob = img.get("blob_path")
        if not rel_blob:
            return None, None, None, 0
        abs_blob = os.path.join(blob_home, rel_blob)
        if not os.path.isfile(abs_blob):
            return None, None, None, 0
        size = os.path.getsize(abs_blob)
        if size <= 0:
            return None, None, None, 0
        with open(abs_blob, "rb") as fh:
            data = fh.read()
        return data, img.get("filename"), img.get("content-type"), size

    def __call__(self):  # NOQA
        alsoProvides(self.request, IDisableCSRFProtection)
        jsonfile = self.request.form.get("jsonfile")
        blob_home = self.request.form.get("blob_home") or ""
        dry_run = bool(self.request.form.get("dry_run"))
        if not jsonfile:
            return (
                "Missing parameter: "
                "?jsonfile=/abs/path/to/_OUTPUT_CONTENTS.json "
                "[&blob_home=/abs/path/to/source/blobstorage] "
                "[&dry_run=1]"
            )

        with open(jsonfile, "rb") as fh:
            data = json.load(fh)

        # UID → item, pour résoudre le canonical par UID puis remonter à son @id.
        by_uid = {it.get("UID"): it for it in data if it.get("UID")}
        clones = [it for it in data if it.get("_clone_blob_from")]
        portal = api.portal.get()

        n_clones = len(clones)
        repaired_from_plone = 0
        repaired_from_export = 0
        already_ok = 0
        clone_missing = 0
        canonical_missing = 0
        canonical_empty = 0
        errors = 0

        logger.info(
            "imio.smartweb.core : reclone_empty_blobs — %s clones à inspecter "
            "(dry_run=%s, blob_home=%s)",
            n_clones,
            dry_run,
            blob_home or "<absent>",
        )

        def commit_if_due(n_done):
            if not dry_run and n_done and (n_done % COMMIT_EVERY) == 0:
                transaction.commit()
                logger.info(
                    "reclone_empty_blobs : %s réparés à ce stade (commit "
                    "intermédiaire)",
                    n_done,
                )

        for item in clones:
            clone_relpath = self._relpath_from_atid(item.get("@id"))
            obj = self._traverse(portal, clone_relpath)
            if obj is None:
                clone_missing += 1
                continue

            if self._blob_size(getattr(obj, "image", None)) > 0:
                already_ok += 1
                continue

            canonical_uid = item["_clone_blob_from"]
            canonical_item = by_uid.get(canonical_uid)
            if canonical_item is None:
                canonical_missing += 1
                logger.warning(
                    "reclone_empty_blobs : canonical UID %s introuvable dans "
                    "le JSON (clone %s)",
                    canonical_uid,
                    clone_relpath,
                )
                continue

            # Voie 1 : canonical présent en Plone à son @id JSON
            canonical_relpath = self._relpath_from_atid(canonical_item.get("@id"))
            source = self._traverse(portal, canonical_relpath)
            source_data = None
            source_filename = None
            source_ctype = None
            source_size = 0
            source_origin = None
            if source is not None:
                source_image = getattr(source, "image", None)
                source_size = self._blob_size(source_image)
                if source_size > 0:
                    source_data = source_image.data
                    source_filename = source_image.filename
                    source_ctype = source_image.contentType
                    source_origin = "plone:" + canonical_relpath

            # Voie 2 (fallback) : lire le blob directement depuis l'export
            if source_data is None:
                xdata, xfname, xctype, xsize = self._read_source_from_export(
                    canonical_item, blob_home
                )
                if xdata is not None:
                    source_data = xdata
                    source_filename = xfname
                    source_ctype = xctype
                    source_size = xsize
                    source_origin = "export:" + (
                        (canonical_item.get("image") or {}).get("blob_path") or ""
                    )

            if source_data is None:
                # Ni Plone ni export. Distinguons les deux cas dans le compteur :
                if source is None:
                    canonical_missing += 1
                    logger.warning(
                        "reclone_empty_blobs : canonical introuvable dans "
                        "Plone à %s (clone %s) — aucun fallback export "
                        "exploitable",
                        canonical_relpath,
                        clone_relpath,
                    )
                else:
                    canonical_empty += 1
                    logger.warning(
                        "reclone_empty_blobs : canonical %s a un blob vide "
                        "— %s non réparable",
                        canonical_relpath,
                        clone_relpath,
                    )
                continue

            if dry_run:
                logger.info(
                    "reclone_empty_blobs (DRY) : %s ← %s (%s octets)",
                    clone_relpath,
                    source_origin,
                    source_size,
                )
                if source_origin.startswith("export:"):
                    repaired_from_export += 1
                else:
                    repaired_from_plone += 1
                continue

            try:
                obj.image = NamedBlobImage(
                    data=source_data,
                    filename=source_filename,
                    contentType=source_ctype,
                )
                obj.reindexObject()
                if source_origin.startswith("export:"):
                    repaired_from_export += 1
                else:
                    repaired_from_plone += 1
                logger.info(
                    "reclone_empty_blobs : %s ← %s (%s octets)",
                    clone_relpath,
                    source_origin,
                    source_size,
                )
            except Exception:
                errors += 1
                logger.exception(
                    "reclone_empty_blobs : échec de réparation pour %s",
                    clone_relpath,
                )
                continue

            commit_if_due(repaired_from_plone + repaired_from_export)

        if not dry_run:
            transaction.commit()

        total_repaired = repaired_from_plone + repaired_from_export
        verb = "à réparer" if dry_run else "réparé(s)"
        msg = (
            "imio.smartweb.core : reclone_empty_blobs — "
            "{} clone(s) inspecté(s) ; {} {} (dont {} via Plone, {} via export) ; "
            "{} déjà OK ; {} clone(s) introuvable(s) en Plone ; "
            "{} canonical(s) introuvable(s) ; "
            "{} canonical(s) aussi vide(s) ; {} erreur(s)"
        ).format(
            n_clones,
            total_repaired,
            verb,
            repaired_from_plone,
            repaired_from_export,
            already_ok,
            clone_missing,
            canonical_missing,
            canonical_empty,
            errors,
        )
        logger.info(msg)
        return msg
