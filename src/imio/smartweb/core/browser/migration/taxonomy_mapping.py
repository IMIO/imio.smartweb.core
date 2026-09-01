# -*- coding: utf-8 -*-
"""Mapping between the old ``page_category`` sub terms and the two new
taxonomies ``avisenquetes`` and ``reglements``.

The Liège site added sub terms under the ``avis_et_enquete`` and ``reglement``
root terms of ``collective.taxonomy.page_category``. Those terms belong to
dedicated taxonomies, so they were re-created in
``collective.taxonomy.avisenquetes`` and ``collective.taxonomy.reglements``
with brand new identifiers.

Keys are the identifiers stored in ``taxonomy_page_category``, values are the
identifiers to store in ``taxonomy_avisenquetes`` / ``taxonomy_reglements``.
Consumed by the one shot ``@@migrate_page_category`` view.
"""

AVISENQUETES_TAXONOMY = "collective.taxonomy.avisenquetes"
REGLEMENTS_TAXONOMY = "collective.taxonomy.reglements"
PAGE_CATEGORY_FIELD = "taxonomy_page_category"
AVISENQUETES_FIELD = "taxonomy_avisenquetes"
REGLEMENTS_FIELD = "taxonomy_reglements"

# Sub terms of the "avis_et_enquete" root term -> collective.taxonomy.avisenquetes
PAGE_CATEGORY_TO_AVISENQUETES = {
    "h89oxm16rd": "t17si8m055",  # Avis d'annonce de projet
    "hl6d8f0uq5": "koadb9cb3p",  # Informations sur l'étude d'incidences
    "smwwjmdre7": "ja003xenra",  # Permis de détention d'explosifs
    "wkh7nco011": "xdf5xbnf5x",  # Permis d'environnement
    "vw627u8ci2": "gahpxyfdbl",  # Permis d'urbanisation
    "93ny1xr4rq": "b8x771g41d",  # Permis d'urbanisme
    "k1m9x7hflb": "uylqc6415e",  # Permis groupés
    "s21slbx3dg": "yr5hvc2e42",  # Permis intégrés
    "slbfv3ir5g": "0wl3gd1vmf",  # Permis unique
    "3qtlcn1anq": "w2yt44q4ly",  # Réunions d'informations publiques
}

# Sub terms of the "reglement" root term -> collective.taxonomy.reglements
PAGE_CATEGORY_TO_REGLEMENTS = {
    "fpswde31ge": "8ly7x1obbc",  # Commerce
    "kuu4hx6dke": "w31k48442h",  # Environnement
    "qfv8apwrp5": "cc82v8yhd1",  # Gestion financière
    "nn6pjbkw4x": "nx3eqati8d",  # ... Taxes et redevances de prestations
    "9eiebk4y0r": "t5jqpy59c6",  # ... Taxes de remboursement
    "ycrflio9jf": "92ixahbp37",  # ... Taxes et redevances d'hygiène publique
    "fy3fp8o1vy": "fc8mi8jmvc",  # ... Taxes et redevances commerciales et industrielles
    "ngeodnosrt": "b95iu72mtw",  # ... Redevances sur l'occupation du domaine public
    "xbal3r7nfm": "jhixku2g7x",  # ... Taxes et redevances sur le patrimoine
    "vmmmskxr86": "svaj719cdm",  # ... Taxes diverses
    "cnij6b4rjr": "mp4d3c9msm",  # ... Taxes additionnelles
    "rxphcyi48i": "sw118s9cca",  # Police administrative
}

# Sub terms without any equivalent in the new taxonomies. They stay as they are
# in collective.taxonomy.page_category. Listed for documentation purpose only.
UNMAPPED_PAGE_CATEGORY_TERMS = {
    "imc5kgi47j",  # Autres enquêtes (avis_et_enquete)
    "2wr317dunf",  # Commerce (avis_et_enquete)
}

# Root term to fall back on in taxonomy_page_category once the precise term has
# been moved to its own taxonomy. page_category is single select, emptying it
# would drop the page out of the navigation listings built on that index.
AVISENQUETES_ROOT_TERM = "avis_et_enquete"
REGLEMENTS_ROOT_TERM = "reglement"
