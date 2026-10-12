# Migration des images inline des SectionText vers des SectionGallery

Date : 2026-06-16
Statut : conception approuvée (en attente de relecture finale)

## Objectif

Fournir une vue de migration qui détecte toutes les `imio.smartweb.SectionText`
contenant au moins une balise `<img>` inline dans leur champ richtext, extrait ces
images vers une `imio.smartweb.SectionGallery` créée dans la page parente, et
retire les `<img>` migrés du richtext. La vue produit un rapport de ce qui a été
trouvé/modifié et fonctionne par défaut en mode dry-run.

## Contexte technique

- `SectionText` (`contents/sections/text/content.py`) possède :
  - un champ richtext `text` (rendu via `context/text/output`),
  - un champ `image` dédié (behavior, rendu en `<figure>` par le template).
  Le `<figure><img>` du champ dédié provient du template, **pas** du HTML stocké.
  Donc un `<img>` présent dans le HTML stocké est une image **inline** insérée
  dans le richtext (TinyMCE). **Seules ces images inline sont concernées.**
- `SectionGallery` (`contents/sections/gallery/content.py`) est un conteneur
  (`manage_content = True`). Sa FTI
  (`profiles/default/types/imio.smartweb.SectionGallery.xml`) n'autorise que des
  enfants de type **`Image`** (`allowed_content_types = Image`). La vue galerie
  itère `listFolderContents` et utilise `item.image`, `item.title`,
  `item.description`.
- Les sections sont des enfants ordonnés de la page (Page / PortalPage), via
  l'ordering de `plone.folder` (`moveObjectToPosition`).
- Pattern de référence existant : `browser/migration/find_broken_links.py`
  (parcours par `api.content.find`, lecture de `obj.text.output`/`.raw`,
  requêtes HTTP avec timeout, `IDisableCSRFProtection`).

## Décisions de conception (validées)

1. **Source des `<img>`** : prise en charge de `resolveuid/<UID>` (images Plone
   internes) et des **URL externes** (http/https). Les data-URI, chemins relatifs
   et URL sur le même portail sont **non supportés** → laissés en place et
   signalés.
2. **Regroupement** : **une `SectionGallery` par SectionText**, positionnée
   immédiatement **après** la SectionText source dans le parent.
3. **Mode** : **dry-run par défaut** ; modifications réelles uniquement avec
   `?apply=1`.
4. **Champ image dédié** : **hors périmètre** — seuls les `<img>` inline du
   richtext sont migrés.
5. **resolveuid** : l'objet `Image` existant est **copié** dans la galerie
   (`api.content.copy`) ; l'original reste intact (évite de casser d'autres
   références à la même image).

## Architecture

Nouveau fichier `browser/migration/migrate_sectiontext_images.py` exposant
`MigrateSectionTextImagesView(BrowserView)`, plus un template
`migrate_sectiontext_images.pt`. Enregistrement dans
`browser/migration/configure.zcml` :

```xml
<browser:page
    for="*"
    name="migrate_sectiontext_images"
    class=".migrate_sectiontext_images.MigrateSectionTextImagesView"
    template="migrate_sectiontext_images.pt"
    permission="cmf.ManagePortal"
    layer="imio.smartweb.core.interfaces.IImioSmartwebCoreLayer"
    />
```

### Fonctions utilitaires (module-level, testables isolément)

- `_extract_img_nodes(raw_html)` → parse le HTML brut avec `lxml.html`, renvoie la
  liste des éléments `<img>` (et le document pour réécriture). Renvoie `([], None)`
  si le HTML est vide ou non parsable.
- `_classify_src(src, portal_url)` → renvoie un type parmi
  `"resolveuid" | "external" | "unsupported"` + la donnée extraite (UID ou URL
  nettoyée). `resolveuid/` détecté n'importe où dans `src` ; UID = segment après
  `resolveuid/` avant `/` ou `?`. http/https hors `portal_url` → `external`.
  Tout le reste (data:, chemins relatifs, même portail) → `unsupported`.
- `_resolve_uid_image(uid)` → renvoie l'objet `Image` (portal_type `Image`) via
  `api.content.find(UID=uid)`, ou `None` si introuvable / mauvais type.
- `_download_external_image(url, cache)` → GET avec timeout (réutilise les
  constantes `_REQUEST_TIMEOUT`/`_USER_AGENT` du pattern existant), renvoie
  `(bytes, filename, content_type)` ou lève/retourne une erreur capturée.
  Mémoïsé dans `cache`.

### Classe de vue

`__call__` :
1. `self.apply = self.request.get("apply") in ("1", "true", "True")`.
2. En mode apply : `alsoProvides(self.request, IDisableCSRFProtection)`.
3. `self.results = []` (une entrée par SectionText concernée), `self.summary`
   (compteurs), `self._download_cache = {}`,
   `self._portal_url = api.portal.get().absolute_url()`.
4. Parcourir `api.content.find(portal_type="imio.smartweb.SectionText")` et
   appeler `self._process_section(obj)`.
5. Calculer `self.summary` et `return self.index()`.

`_process_section(obj)` :
1. Lire `richtext = getattr(obj, "text", None)` ; si `None`/vide → ignorer.
2. `nodes, doc = _extract_img_nodes(richtext.raw)` ; si aucun `<img>` → ignorer.
3. Pour chaque node : classifier `src`, déterminer l'action et le statut.
   - `unsupported` → statut `skipped`, raison, **node conservé**.
   - `resolveuid` introuvable → statut `failed`, **node conservé**.
   - `external` en échec de téléchargement → statut `failed`, **node conservé**.
   - sinon → statut `migrated` (apply) / `to_migrate` (dry-run), node marqué pour
     suppression.
4. S'il existe ≥ 1 image migrable **et** mode apply :
   - Créer la galerie : `api.content.create(container=parent, type=
     "imio.smartweb.SectionGallery", title="Galerie — {obj.title}")`.
   - Repositionner juste après la SectionText :
     `parent.moveObjectToPosition(gallery.getId(), parent.getObjectPosition(obj.getId()) + 1)`.
   - resolveuid → `api.content.copy(source=image_obj, target=gallery)`.
   - external → `api.content.create(container=gallery, type="Image",
     title=<alt ou filename>, image=NamedBlobImage(data=bytes,
     filename=filename, contentType=content_type))`.
   - Retirer du DOM uniquement les `<img>` à statut `migrated` (drop du node, via
     `node.drop_tree()`), puis réécrire :
     `obj.text = RichTextValue(serialized_raw, richtext.mimeType,
     richtext.outputMimeType)` et `obj.reindexObject()`.
5. Enregistrer l'entrée de résultat (chemin SectionText, chemin parent, titre
   galerie, liste d'images avec type/source/statut/raison).

### Positionnement & idempotence

- Positionnement via `getObjectPosition` / `moveObjectToPosition` du conteneur
  ordonné (`plone.folder`). Si `moveObjectToPosition` n'est pas disponible sur le
  parent, fallback : laisser la galerie en fin (et le signaler au rapport).
- **Idempotence naturelle** : après un apply réussi, la SectionText n'a plus de
  `<img>` migrable, donc elle n'est pas reprise au passage suivant. Les images en
  échec restent et peuvent être retentées.

## Rapport (template .pt)

- En-tête : mode (DRY-RUN / APPLIQUÉ), avec lien explicite vers `?apply=1` en
  dry-run.
- Synthèse : nb de SectionText concernées, nb d'images par statut
  (migrated/to_migrate, failed, skipped), nb de galeries créées.
- Tableau détaillé par SectionText : chemin (lien), parent, titre galerie, puis
  pour chaque image : type, source (UID/URL), statut, raison d'échec/skip.

## Gestion d'erreurs

- HTML non parsable → SectionText ignorée silencieusement (cohérent avec
  `find_broken_links`).
- Téléchargement externe : `Timeout`, `SSLError`, `ConnectionError`, exceptions
  génériques → capturées, message tronqué, statut `failed`, `<img>` conservé.
- Échec de création d'`Image`/galerie → capturé par SectionText, reporté ; la
  SectionText n'est pas modifiée si la galerie n'a pu être peuplée.
- Aucune image migrable dans une SectionText → aucune galerie créée.

## Tests (suivre le skill plone-testing)

Classe `TestMigrateSectionTextImages(ImioSmartwebTestCase)`, layer
`IMIO_SMARTWEB_CORE_INTEGRATION_TESTING`, `setRoles([..., "Manager"])`.

Cas couverts :
1. SectionText avec `<img src="resolveuid/UID">` pointant vers un `Image`
   existant → dry-run ne modifie rien et rapporte `to_migrate` ; apply crée une
   `SectionGallery` après la SectionText, contenant une copie de l'`Image`, et le
   richtext ne contient plus l'`<img>`.
2. SectionText avec `<img>` externe (mock via `requests_mock`) → apply crée un
   `Image` dans la galerie depuis les octets téléchargés ; échec réseau → `failed`,
   `<img>` conservé, pas de galerie.
3. SectionText avec `<img>` data-uri / chemin relatif → `skipped`, conservé.
4. SectionText sans `<img>` → ignorée, aucune galerie.
5. Idempotence : deux applies successifs → une seule galerie, pas de doublon.
6. Positionnement : la galerie est bien l'élément suivant la SectionText dans le
   parent.
7. Permission : la vue exige `cmf.ManagePortal`.

## Hors périmètre

- Migration du champ `image` dédié de SectionText.
- Images en data-URI, chemins relatifs, ou même portail (signalées, non migrées).
- Déduplication d'images identiques entre SectionText différentes.
- Suppression des objets `Image` source d'origine (on copie, on ne déplace pas).
