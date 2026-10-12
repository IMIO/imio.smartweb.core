# Dedicated ODWB widget section — design

Date: 2026-07-22
Package: `imio.smartweb.core`
Status: approved (brainstorming)

## Problem

Editors can already embed OpenDataSoft / ODWB (Open Data Wallonie-Bruxelles)
widgets — but only by hand-pasting raw AngularJS `<ods-*>` markup into the
generic `external_content_params` field of a `SectionExternalContent`, whose
`OdwbWidgetPlugin` matches `static.opendatasoft.com` URLs. That path is buried,
undiscoverable, and offers no validation.

We want a dedicated, cleaner section type for pasting ODWB widget markup, with
proper validation and a permission-gated field. It **coexists** with the
existing `SectionExternalContent` ODWB plugin (no deprecation, no data
migration).

## Scope

In scope:

- A new section type `imio.smartweb.SectionODWB`.
- A single raw-markup field, permission-gated.
- Structural validation of the pasted markup on save.
- Reuse of the existing AngularJS ODS-Widgets rendering stack.

Explicitly **out of scope** (YAGNI):

- No structured widget builder (dataset/type/params form).
- No ODS Explore API v2.1 / ODSQL querying.
- No native / React / Leaflet rendering of ODS data.
- No migration of existing `SectionExternalContent` ODWB instances.
- No live edit-mode preview.

## Key constraint: how the ODS library loads

Loading the ODS stack (jQuery + AngularJS 1.8.2 + angular-sanitize +
`ods-widgets.min.js/css`) **twice on one page** would double-bootstrap
AngularJS and break rendering. The existing mechanism loads it exactly once:

1. `subscribers.py:added_external_content` marks the parent **page** with the
   `IOdwbViewUtils` interface (`alsoProvides`) when a `SectionExternalContent`
   is added; `removed_external_content` strips the marker when zero remain.
2. The `odwb_widget_header` viewlet is registered `for="IOdwbViewUtils"` in the
   `IHTTPHeaders` manager, so a page carrying that marker injects the ODS stack
   into its `<head>` once.

Therefore the new section **shares the same `IOdwbViewUtils` marker and the same
viewlet** rather than introducing its own — this is what prevents a double-load
when a page contains both an old ExternalContent-ODWB section and a new
`SectionODWB`.

## Design

### Content type

- FTI name: `imio.smartweb.SectionODWB`
- Interface: `ISectionODWB` (extends `ISection`)
- Class: `SectionODWB(Section)`
- Package dir: `contents/sections/odwb/` (`content.py`, `view.pt`,
  `configure.zcml`, `__init__.py`)

### Schema (`contents/sections/odwb/content.py`)

- `odwb_widget_code` — `schema.SourceText`, `required=True`,
  `write_permission("imio.smartweb.core.CanManageSectionODWB")`. Field help text
  briefly points to odwb.be's widget export tab.
- `description` — `schema.Text`, optional, `max_length=DESCRIPTION_MAX_LENGTH`
  (mirrors `SectionHTML` / `SectionExternalContent`).
- Inherits base `Section` fields: `hide_title`, `collapsible_section`,
  `background_image`, `bootstrap_css_class`, `css_class`.

### Structural validation

An `@invariant` on `ISectionODWB` raises `Invalid` with a clear, translated
message when `odwb_widget_code` contains no `ods-dataset-context` tag:

```python
@invariant
def validate_odwb_widget_code(data):
    code = data.odwb_widget_code or ""
    if "ods-dataset-context" not in code:
        raise Invalid(_("The ODWB widget code must contain an "
                        "<ods-dataset-context> widget."))
```

### Rendering (`view.pt`)

- View class: reuse `SectionView`.
- Template follows the standard section container / `section_title` /
  collapsible macros (like `html/view.pt`), then wraps the code in the existing
  ng-app pattern (as `view_odwb_widget.pt` does):

```html
<div ng-cloak ng-app="ods-widgets">
  <div tal:content="structure context/odwb_widget_code" />
</div>
```

- Library loading: a subscriber on `ISectionODWB` add/remove marks/unmarks the
  parent page with the existing `IOdwbViewUtils`. No new viewlet.

### The one existing-code touch (correctness)

`removed_external_content` currently strips `IOdwbViewUtils` when zero
`SectionExternalContent` remain in the parent. Because `SectionODWB` now shares
that marker, the un-mark decision must count **both**
`SectionExternalContent` **and** `SectionODWB` descendants before removing the
marker. Refactor the count into a small shared helper used by both the
external-content removal handler and the new ODWB removal handler.

New subscribers (in `contents/sections/odwb/` or `subscribers.py`, following the
existing external-content pattern):

- `added_odwb` — `alsoProvides(parent, IOdwbViewUtils)` if not already provided.
- `removed_odwb` — `noLongerProvides` only when the shared helper reports zero
  ODWB-bearing sections (both types) remain.

## Wiring — full "anatomy of a section" (all additive except §"one touch")

- `contents/sections/odwb/` → `content.py`, `view.pt`, `configure.zcml`,
  `__init__.py` (browser:page `view` registration mirrors `html/configure.zcml`).
- `contents/__init__.py` → import `ISectionODWB` / `SectionODWB`.
- `contents/sections/configure.zcml` → `<include package=".odwb" />` and the
  add/remove subscriber registrations for `ISectionODWB`.
- `permissions.zcml` → new permission
  `imio.smartweb.core.CanManageSectionODWB`.
- `profiles/default/rolemap.xml` → grant `CanManageSectionODWB` to `Manager`,
  `Site Administrator`, `Local Manager` (mirrors `CanManageSectionHTML`).
- `profiles/default/types.xml` → register `imio.smartweb.SectionODWB`.
- `profiles/default/types/imio.smartweb.SectionODWB.xml` → FTI: title/description,
  `icon_expr`, `global_allow=False`, `filter_content_types=True`,
  `allowed_content_types` (Image, File),
  `add_permission=imio.smartweb.core.CanManageSectionODWB`,
  `klass=...contents.SectionODWB`, `schema=...contents.ISectionODWB`,
  behaviors (`plone.namefromtitle`, `plone.locking`, `plone.shortname`).
- `profiles/default/types/imio.smartweb.Page.xml`,
  `...PortalPage.xml`, `...Procedure.xml` → add `imio.smartweb.SectionODWB` to
  `allowed_content_types`.
- `profiles/default/registry/plone.xml` → add to the section-ordering list.
- `profiles/icons/contenttypes/registry.xml` → icon entry (reuse an existing SVG
  initially).
- Upgrade step (new profile version) → registers type + permission + rolemap +
  allowed_content_types + registry ordering on existing sites. Additive; no data
  migration.
- Locales: new i18n message ids (title, description, field labels, invariant
  message) added to `imio.smartweb.locales` in the normal release flow.

## Testing (`tests/test_section_odwb.py`)

Follow the `plone-testing` skill. Cover:

- Type is installed and addable in `Page` / `PortalPage` / `Procedure`
  (FTI + `allowed_content_types`).
- Invariant: rejects markup with no `ods-dataset-context`; accepts valid markup.
- Marker behavior: adding a `SectionODWB` makes the parent provide
  `IOdwbViewUtils`; removing the last ODWB-bearing section removes it.
- **Mixed-section removal case**: a page with one `SectionExternalContent`
  (ODWB) and one `SectionODWB` keeps `IOdwbViewUtils` when only one of the two
  is removed, and loses it only when both are gone.
- Permission: `odwb_widget_code` write / type add are gated by
  `CanManageSectionODWB`.
- View: renders the markup wrapped in the `ng-app="ods-widgets"` container.

## Open decisions resolved

- Naming: `SectionODWB` / `CanManageSectionODWB` (confirmed).
- Coexist with the existing ExternalContent ODWB plugin; no migration (confirmed).
- UX/validation: structural validation + permission-gated field only; no inline
  example, no edit-mode preview note (confirmed).
