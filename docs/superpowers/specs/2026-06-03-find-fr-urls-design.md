# Design : vue de migration `find_fr_urls`

**Date :** 2026-06-03
**Statut :** validé par l'utilisateur

## Objectif

Fournir une vue de migration qui liste toutes les URLs contenant la chaîne
`/fr/` présentes dans le contenu des objets `imio.smartweb.SectionText` et
`imio.smartweb.SectionHTML`, afin d'identifier les liens à corriger après
migration.

## Périmètre

- **Types scannés :**
  - `imio.smartweb.SectionText` → champ richtext `text` (HTML rendu
    `output`, repli sur `raw`)
  - `imio.smartweb.SectionHTML` → champ `html`
- **URLs retenues :** valeurs des attributs `href` (balises `<a>`) et `src`
  (`<img>`, `<iframe>`, …) contenant la sous-chaîne `/fr/`.
- **Hors périmètre :** occurrences de `/fr/` dans le texte visible ou les
  styles inline ; aucune vérification HTTP ; aucune modification de contenu
  (vue en lecture seule).

## Conception

- **Fichier :** `src/imio/smartweb/core/browser/migration/find_fr_urls.py`
- **Classe :** `FindFrUrlsView(BrowserView)`
- **Nom de vue :** `@@find_fr_urls`, permission `cmf.ManagePortal`,
  layer `IImioSmartwebCoreLayer` (déclaration dans
  `browser/migration/configure.zcml`)
- **Extraction :** `lxml.html` + xpath `//a/@href | //*/@src`, filtrage des
  valeurs contenant `/fr/`
- **Template :** `find_fr_urls.pt`, table HTML sur le modèle de
  `find_broken_links.pt` avec colonnes :
  1. URL de l'objet (lien cliquable)
  2. Type de contenu (`portal_type`)
  3. URL trouvée
  4. Attribut source (`href` ou `src`)

  Plus un compteur du nombre total d'URLs trouvées.

## Approches écartées

- Étendre `find_broken_links` avec un paramètre : mélange deux
  responsabilités et complique les deux vues.
- Sortie CSV/JSON : moins pratique pour un usage humain ; les vues sœurs du
  dossier rendent du HTML.

## Tests

Pas de tests dédiés : alignement sur les autres vues de migration du dossier
(`find_broken_links`, `find_section_selections`) qui n'en ont pas.

## Gestion des erreurs

- HTML non parsable → ignoré silencieusement (même comportement que
  `_extract_hrefs` de `find_broken_links`).
- Champ `text`/`html` absent ou vide → objet ignoré.
