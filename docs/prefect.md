# `@prefect` — editorial content of a page, as JSON

Ticket: WEB-4524
Implementation: `src/imio/smartweb/core/rest/prefect.py`
Tests: `src/imio/smartweb/core/tests/test_rest_prefect.py`
Contract version: `schema_version: 1`

`@prefect` gives the editorial content of a SmartWeb page as a simple JSON
document. The Prefect ETL reads it and converts it to Markdown. The endpoint
does **not** produce Markdown: the conversion is the job of the consumer.

The JSON is a contract that is independent of the internal structures of Plone
and SmartWeb. It does not contain presentation data (widths, CSS classes,
carousel settings, image scales, icons…).

---

## 1. Endpoint

```
GET {page_url}/@prefect
Accept: application/json
```

| Content type | Eligible |
|---|---|
| `imio.smartweb.Page` | yes |
| `imio.smartweb.PortalPage` | yes |
| `imio.smartweb.Procedure` | yes |
| `imio.smartweb.Footer`, `imio.smartweb.HeroBanner`, any other type | no (404) |

Footer and HeroBanner are parts of other pages, not documents. Their content is
never added to the JSON of a page.

| HTTP status | Meaning |
|---|---|
| 200 | The JSON document below. |
| 401 | The user cannot view the page (for example a private page, anonymous user). |
| 404 | The URL is not an eligible page, or it does not exist. |
| 500 | Unexpected error outside the sections (for example in `metadata`). |

**Permissions.** The endpoint gives only what the user who calls it can view.
The recommended caller is **anonymous**: the ETL then gets the public content
only. If unpublished content is necessary, use a dedicated technical account
with the Reader role, never an administrator account.

**What the endpoint does not do.**
- It does not use the HTML rendering views.
- It calls only one external service: **imio.directory**, for the contact
  sections (§3.5). It does not call imio.events, imio.news, iA.Delib, oEmbed…:
  that remote content is given as references (see §4).
- It does not compute image scales and does not read file data.

---

## 2. Document structure

```json
{
  "schema_version": 1,
  "uid": "3f1c9e0a8b2d4c6e9f7a1b2c3d4e5f60",
  "url": "https://www.commune.be/environnement/collecte-des-dechets",
  "type": "page",
  "language": "fr",
  "title": "Collecte des déchets",
  "description": "Calendrier et **règles de tri**",
  "modified": "2026-10-21T09:14:03+00:00",
  "procedure_url": null,
  "metadata": { "...": "see §2.2" },
  "sections": [ "...see §3 and §4" ]
}
```

### 2.1 Root fields

| Key | Type | Description |
|---|---|---|
| `schema_version` | integer | Version of this contract. See §8. |
| `uid` | string | Plone UID of the page. **Stable identifier** of the document (see §6.1). |
| `url` | string | Absolute URL of the page. It changes when the page or a parent folder is moved or renamed. |
| `type` | string | `"page"`, `"portal_page"` or `"procedure"`. |
| `language` | string | Language of the page. If the page has no language, the default language of the site. |
| `title` | string | Title of the page. |
| `description` | string \| null | Description, raw (see §5.4). |
| `modified` | string | Last modification date of the page, ISO 8601, UTC, to the second. See §7.2. |
| `procedure_url` | string \| null | Procedure only: URL of the online form (e-guichet form or manual URL). `null` for other types. |
| `metadata` | object | See §2.2. |
| `sections` | array | The sections, **in the order of the page**. See §3. |

### 2.2 `metadata`

The editorial characteristics of the page. They come from the parent folders
or from the page fields.

| Key | Type | Description |
|---|---|---|
| `minisite` | `{title, url}` \| null | The minisite that contains the page. In the user interface, a minisite is called a **"site partenaire"**. |
| `subsite` | `{title, url}` \| null | The subsite ("sous-site") that contains the page, searched up to the first navigation root (the site or a minisite). |
| `category` | string \| null | Label of the category (taxonomy), as the category viewlet shows it. Always `null` for `portal_page`. |
| `topics` | string[] | Labels of the topics ("thématiques"). |
| `iam` | string[] | Labels of the "I am" ("Je suis") profiles. |

A minisite or subsite folder that the user cannot view is given as `null`.
Terms that do not exist anymore in a vocabulary are not given.

---

## 3. Sections

### 3.1 Common fields

Each item of `sections` has these fields:

| Key | Type | Description |
|---|---|---|
| `id` | string | Identifier of the section in the page. The section is visible at `{page_url}#section-{id}`. |
| `type` | string | Type of the section (see §3.3 and §4). |
| `status` | string | `"ok"`, `"unsupported"` or `"error"` (see §3.2). |
| `title` | string \| null | Title of the section. |
| `title_hidden` | boolean | `true` if the editor hid the title for visitors. The title stays in the JSON: the consumer decides what to do with it. |

### 3.2 `status`

| Value | Meaning | Specific fields | What to do |
|---|---|---|---|
| `"ok"` | The section is serialized as this contract defines it. It can be empty (`[]`, `null`). | present | Use it. |
| `"unsupported"` | The section type is not part of this contract version (for example a new type added later). | absent | Ignore the section and log it. The document is complete. |
| `"error"` | The serialization of this section failed. The error is logged on the server; the JSON does not contain the details. | absent | **The document is incomplete**: do not overwrite the previous Markdown (see §6.3). |

The specific fields of §3.3 and §4 are present **only** when `status` is `"ok"`.

### 3.3 Sections with editorial content

| `type` | Specific fields |
|---|---|
| `text` | `html`: string \| null — `iframes`: Iframe[] — `image`: `{url, caption}` \| null |
| `html` | `description`: string \| null — `html`: string \| null — `iframes`: Iframe[] |
| `links` | `description`: string \| null — `links`: `[{title, description, url, internal}]` |
| `gallery` | `images`: `[{url, title, description}]` |
| `files` | `files`: `[{title, description, url, mime_type, size}]` |
| `video` | `description`: string \| null — `video_url`: string |
| `map` | `latitude`: number \| null — `longitude`: number \| null |
| `postit` | `description`: string \| null — `postits`: `[{title, subtitle, description}]` |
| `selections` | `items`: `[{title, description, url}]` |
| `external_content` | `description`: string \| null — `url`: string |

`Iframe` is `{url, title}`: `url` is an absolute `http`/`https` URL, `title` is
the `title` attribute of the iframe, or `null`.

Details:

- **`text`** — `image` is the image of the section (`url` of the original
  image, `caption` or `null`).
- **`html`** — the HTML that an editor entered, cleaned (see §5.2).
- **`links`** — `url` is `null` when the link cannot be followed: internal
  target deleted or not visible to the user, or forbidden scheme (see §5.1).
  The link stays in the list with its title. `internal` is `true` for a link to
  content of the site (also when its target cannot be followed), `false` for an
  external link.
- **`gallery`** — `title` is `null` when the title is only the file name of the
  image. There is no "alternative text" field in SmartWeb: use `description`,
  else `title`.
- **`files`** — a file of the site gives its download URL, `mime_type` and
  `size` (bytes). A publication (iA.Delib) gives the public URL of the
  publication in iA.Delib, and `mime_type` and `size` of its attached file, as
  stored when it was added to the section.
- **`video`** — no video title: the title is not stored, only the URL
  (YouTube, Vimeo…).
- **`map`** — the point of the map section. No address is stored.
- **`selections`** — contents chosen by the editor. A content that the user
  cannot view, or that does not exist anymore, is **not** in `items`.
- **`external_content`** — URL of the embedded service (widget, form, map…).
  The technical parameters of the widget are not given.

### 3.5 `contact`

| Key | Type | Description |
|---|---|---|
| `contact_uids` | string[] | UIDs of the contacts chosen by the editor, in the order of the section. |
| `contacts` | Contact[] | The contacts as the section shows them, in the same order. |

The endpoint gets the contacts from **imio.directory**, in one request for the
section, as an anonymous visitor (only published contacts). A contact that the
directory does not give (deleted, not published, unknown) is in `contact_uids`
but not in `contacts`, as on the site. An empty `contacts` is a legitimate
result.

If imio.directory does not answer (connection error, timeout of 10 seconds,
HTTP error, invalid JSON), the section gets `status: "error"`: the document is
incomplete (§6.3). It never looks empty because of an error.

**Visible blocks.** In each contact section, the editor chooses the blocks
that the site shows ("visible blocks"). A `Contact` gives **only** the data of
these blocks. The keys of a hidden block are always present, with `null` or
`[]`, even when the directory has the data.

| Block | Keys of `Contact` |
|---|---|
| (always) | `uid` |
| Title and subtitle | `title`, `subtitle` |
| Contact informations | `vat_number`, `phones`: `[{label, type, number}]`, `emails`: `[{label, type, address}]`, `urls`: `[{type, url}]` |
| Address | `address`: `{street, locality, country}` \| null |
| Itinerary | `itinerary_url`: string \| null (Google Maps directions) |
| Schedule | `schedule`: Schedule \| null (`null` also when no hours are entered) |
| Map | `location`: `{latitude, longitude}` \| null |
| Description | `description`: string \| null (raw, see §5.4) |
| Logo | `logo_url`: string \| null |
| Lead image | `image_url`: string \| null |
| Gallery | `images`: `[{url, title, description}]` |

`Schedule` is the opening hours as entered in the directory:

```json
{
  "days": [
    { "day": "monday", "hours": "08:00 - 12:00 | 13:00 - 15:00 (Ouverture classique)" },
    { "day": "sunday", "hours": "Closed" }
  ],
  "periods": [
    {
      "dates": [ { "start": "2026-07-01", "end": "2026-08-31" } ],
      "days": [ { "day": "monday", "hours": "09:00 - 12:00" } ]
    }
  ],
  "closures": [ { "date": "2026-12-24", "title": "Christmas Eve" } ]
}
```

- `days`: the regular week, Monday to Sunday. `hours` is formatted as on the
  site; it is translated "Closed" when there are no hours.
- `periods`: other hours for some date ranges (for example summer).
- `closures`: days when the place is closed.

The site shows the next 7 days from today, with the periods and closures
applied, and an "open now" message. The endpoint gives the stored data
instead: the result of the site changes every day, which would change the
document every day.

When the gallery block is visible, the endpoint does one more request to
imio.directory for each contact, to get its images (as the site does).

### 3.6 Example of `links`

```json
{
  "id": "liens-utiles", "type": "links", "status": "ok",
  "title": "Liens utiles", "title_hidden": false, "description": null,
  "links": [
    { "title": "Recyparcs", "description": "Horaires", "url": "https://www.commune.be/recyparcs", "internal": true },
    { "title": "Guide du tri", "description": null, "url": "https://www.fostplus.be/fr/trier", "internal": false },
    { "title": "Ancien règlement", "description": null, "url": null, "internal": true },
    { "title": "Service population", "description": null, "url": "mailto:population@commune.be", "internal": false }
  ]
}
```

---

## 4. Sections with dynamic, remote or referenced content

These sections show content that SmartWeb computes or gets from another
application when the page is rendered. The endpoint gives **references only**,
never the computed content, for two reasons: the content changes without a
change of the page (§7.1), and getting it needs network calls.

| `type` | Specific fields | How to get the content |
|---|---|---|
| `timestamped_publications` | `publication_uids`: string[] — `publications_source_url`: string \| null | UIDs of publications in **iA.Delib**. `publications_source_url` is the URL of the institution of the site in iA.Delib (the base for a search). Only published publications are shown on the site: apply the same filter and accept unknown UIDs. |
| `collection` | `link_text`: string \| null — `url`: string \| null | Link "see all" to the collection. |
| `events` | `link_text`: string \| null — `url`: string \| null | Link "see all" to the events view of the site. |
| `news` | `link_text`: string \| null — `url`: string \| null | Link "see all" to the news view of the site. |

For `collection`, `events` and `news`, `url` is `null` when the target does not
exist or the user cannot view it.

`HeroBanner` slides (`imio.smartweb.SectionSlide`) cannot be in an eligible
page.

---

## 5. Conventions

### 5.1 URLs

- All URLs are **absolute**.
- Internal links (`resolveuid` links, `${portal_url}` variables, relative
  URLs) are resolved by the endpoint. The consumer never resolves a Plone
  reference.
- Internal links are resolved **with the permissions of the user**. A link to
  content that is deleted or that the user cannot view does not give its URL.
- Accepted schemes:

  | Where | Schemes |
  |---|---|
  | Links (`links[].url`, `<a href>` in HTML) | `http`, `https`, `mailto`, `tel` |
  | Images (`<img src>` in HTML) | `http`, `https` |
  | Iframes (`iframes[].url`) | `http`, `https` |

- An image or a link URL of the site points to the original data:
  `{content_url}/@@images/image` (images), `{content_url}/@@download/file`
  (files).

### 5.2 HTML (`text.html`, `html.html`)

The HTML keeps the editorial structure: paragraphs, headings, lists, links,
emphasis, tables, images. The endpoint cleans it with fixed rules that do
**not** depend on the filter settings of the site:

- Removed: scripts, styles, comments, form fields, embedded objects and frames.
  The text around them stays.
- `<iframe>`: removed from the HTML and given in `iframes` (when their URL is
  `http`/`https`). The position of an iframe in the HTML is not kept: render
  `iframes` after the HTML.
- Attributes: only `href`, `src`, `alt`, `title`, `colspan`, `rowspan` stay. No
  `class`, `style`, `on*` (JavaScript) attributes.
- A link that cannot be followed (§5.1) is removed, **its text stays**.
- An image with a forbidden or unresolved URL is removed.

The HTML is safe to convert (for example with `markdownify` or `html2text`).

### 5.3 Absent values

- An optional value that is absent: `null`.
- A collection that is empty: `[]`.
- An empty string is given as `null`.
- All the keys of a type are always present when `status` is `"ok"`.

### 5.4 Descriptions

`description` fields (page, sections, links, images, post-its…) are plain text.
Editors can use `**text**` for bold: it is already Markdown, keep it as it is.

---

## 6. Rules for the consumer (Prefect)

### 6.1 Identity

Use **`uid`** as the identifier of a document. Do not use `url`: it changes
when a page or a parent folder is moved or renamed. Store `url` as a property
of the document.

### 6.2 Canonical hash

To know if a document changed, compute a hash of the JSON **without the root
key `modified`**. `modified` can change when the content does not change (§7.2):
including it would cause artificial updates.

```python
import hashlib
import json


def content_hash(document):
    data = {key: value for key, value in document.items() if key != "modified"}
    canonical = json.dumps(
        data, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
```

Do not sort the arrays: the order of `sections`, `links`, `images`… is part of
the content.

### 6.3 Errors

- A document with **at least one section with `status: "error"`** is
  **incomplete**. Do not overwrite the previous Markdown of this `uid`. Log the
  error and try again at the next run.
- A response that is not HTTP 200 follows the same rule.
- A section with `status: "unsupported"` does not make the document incomplete.

### 6.4 Incremental run and reconciliation

Use two types of runs:

1. **Incremental run** (frequent). Find the pages modified since the last
   run, then get `@prefect` for each one:

   ```
   GET {site_url}/@search
       ?portal_type=imio.smartweb.Page
       &portal_type=imio.smartweb.PortalPage
       &portal_type=imio.smartweb.Procedure
       &modified.query=2026-11-03T00:00:00
       &modified.range=min
       &metadata_fields=UID
       &b_size=100
   ```

   Follow the `batching` links to get all the results.

2. **Reconciliation** (every night). Get the full list of eligible pages (same
   search without `modified`), get `@prefect` for all of them, and compare
   the hash (§6.2) with the stored hash. Regenerate the Markdown only when the
   hash changed.

The reconciliation finds the changes that the incremental run cannot see
(§7.1), and the deleted or unpublished pages.

### 6.5 Deleted and unpublished pages

- An **incomplete enumeration is not a proof of deletion**. If the search
  fails, times out, or gives fewer results than `items_total`, do not delete
  anything.
- **Confirm a disappearance** before you delete a document: search the UID
  (`@search?UID={uid}`), and/or get `@prefect` on the stored URL (401 or 404).
  For more safety, delete only after two reconciliations that do not find the
  page.
- For an anonymous caller, an unpublished page disappears like a deleted page.
  This is the expected result for a public corpus.

---

## 7. Known limits

### 7.1 Referenced data

The JSON can change while `modified` of the page does not change, because some
data comes from other contents:

| Cause | Effect in the JSON |
|---|---|
| Title, description or URL of a selected content changes | `selections.items` |
| Internal link target moved, deleted or made private | `url` changes or becomes `null`; link removed from HTML |
| The page or a parent folder is moved or renamed | `url` and all the URLs of the site in the document |
| Minisite or subsite activated, deactivated or renamed | `metadata.minisite`, `metadata.subsite` |
| Label of a category, topic or "I am" term changes | `metadata` |
| Workflow change of the page | visibility of the page |

The nightly reconciliation (§6.4) finds these changes. There is no propagation
of modifications from referenced contents to the pages that use them.

### 7.2 `modified`

`modified` is the date of the last change of **the page itself, its sections
and the contents of its sections**. These actions update it:

- edit of the page;
- add, edit, delete or reorder of a section;
- hide or show of a section title;
- add, edit or delete of a content in a section (link, image, file,
  publication).

`modified` can also change without a change of the JSON (for example a change
of section width, or an editor who views a page with events or news whose
remote data changed). This is not a problem: the hash (§6.2) does not change.

### 7.3 Remote content

Events, news and timestamped publications are references only (§4). The JSON
does not show if a referenced item still exists in the remote application.

Contacts (§3.5) come from imio.directory at each request. They can change in
the directory with no change of the page: `modified` does not show it. The
nightly reconciliation (§6.4) finds these changes. There is no propagation of
modifications from imio.directory to SmartWeb.

A page with contact sections depends on imio.directory: when the directory is
not available, these sections are in error and the document is incomplete.

---

## 8. Changes to the contract

- **Additions** (a new section type, a new key) do not change
  `schema_version`. The consumer must accept unknown keys and treat an unknown
  `type` like `status: "unsupported"`.
- **Breaking changes** (a key renamed or removed, a different meaning, a
  different type) increase `schema_version`.
- Each `type` has a contract test in `test_rest_prefect.py` that checks its
  exact keys: a change of the contract must update this file.

---

## 9. Complete example

```json
{
  "schema_version": 1,
  "uid": "3f1c9e0a8b2d4c6e9f7a1b2c3d4e5f60",
  "url": "https://www.commune.be/environnement/collecte-des-dechets",
  "type": "page",
  "language": "fr",
  "title": "Collecte des déchets",
  "description": "Calendrier, points de collecte et **règles de tri**.",
  "modified": "2026-10-21T09:14:03+00:00",
  "procedure_url": null,
  "metadata": {
    "minisite": null,
    "subsite": { "title": "Environnement", "url": "https://www.commune.be/environnement" },
    "category": "Environnement",
    "topics": ["Environnement et propreté"],
    "iam": ["Nouvel arrivant"]
  },
  "sections": [
    {
      "id": "horaires", "type": "text", "status": "ok",
      "title": "Horaires de collecte", "title_hidden": false,
      "html": "<p>Sortez les sacs <strong>la veille après 18 h</strong>.</p><h3>Jours fériés</h3><ul><li>1er novembre : collecte le samedi</li></ul>",
      "iframes": [],
      "image": { "url": "https://www.commune.be/environnement/collecte-des-dechets/horaires/@@images/image", "caption": "Camion de collecte" }
    },
    {
      "id": "carte", "type": "html", "status": "ok",
      "title": "Carte interactive", "title_hidden": false,
      "description": "Découvrez **les points d'apport**.",
      "html": "<p>Consultez les points d'apport sur cette carte.</p>",
      "iframes": [ { "url": "https://carto.example.be/collectes", "title": "Carte des points d'apport" } ]
    },
    {
      "id": "documents", "type": "files", "status": "ok",
      "title": "Documents", "title_hidden": false,
      "files": [
        { "title": "Règlement 2026", "description": null, "url": "https://www.commune.be/environnement/collecte-des-dechets/documents/reglement-2026.pdf/@@download/file", "mime_type": "application/pdf", "size": 248113 }
      ]
    },
    {
      "id": "video-tri", "type": "video", "status": "ok",
      "title": "Bien trier en 2 minutes", "title_hidden": false,
      "description": null, "video_url": "https://www.youtube.com/watch?v=abc123"
    },
    {
      "id": "contact", "type": "contact", "status": "ok",
      "title": "Service environnement", "title_hidden": false,
      "contact_uids": ["a1b2c3d4e5f60718293a4b5c6d7e8f90"],
      "contacts": [
        {
          "uid": "a1b2c3d4e5f60718293a4b5c6d7e8f90",
          "title": "Service environnement", "subtitle": null,
          "vat_number": null,
          "phones": [ { "label": "Accueil", "type": "work", "number": "+32 81 00 00 00" } ],
          "emails": [ { "label": null, "type": "work", "address": "environnement@commune.be" } ],
          "urls": [],
          "address": { "street": "Rue de l'Hôtel de Ville 1", "locality": "5000 Namur", "country": "Belgique" },
          "itinerary_url": "https://www.google.com/maps/dir/?api=1&destination=Rue de l'Hôtel de Ville+1+5000+Namur+Belgique",
          "schedule": {
            "days": [ { "day": "monday", "hours": "08:30 - 12:00" } ],
            "periods": [],
            "closures": []
          },
          "location": null, "description": null,
          "logo_url": null, "image_url": null, "images": []
        }
      ]
    },
    {
      "id": "localisation", "type": "map", "status": "error",
      "title": "Localisation", "title_hidden": false
    }
  ]
}
```

This document is **incomplete** (the `map` section has `status: "error"`):
following §6.3, Prefect keeps the previous Markdown of this page.
