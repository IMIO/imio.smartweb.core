# ODWB Widget Section Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **REQUIRED SUB-SKILL for every task that touches a test file:** invoke `plone-testing` before writing/modifying tests in this package.

**Goal:** Add a dedicated `imio.smartweb.SectionODWB` section type for pasting OpenDataSoft/ODWB `<ods-*>` widget markup, with a permission-gated field, structural validation, and reuse of the existing AngularJS ODS-Widgets rendering stack.

**Architecture:** A standard SmartWeb Dexterity "Section" content type (mirrors `SectionHTML`). Rendering reuses the existing `IOdwbViewUtils` marker + `odwb_widget_header` viewlet that already injects the ODS stack once per page — the new section shares that marker so AngularJS is never double-loaded. Coexists with the existing `SectionExternalContent` ODWB plugin; the only existing-code change is making the marker-removal decision count both section types.

**Tech Stack:** Plone 6.1.3 / Dexterity, zope.schema, zope.interface invariants, GenericSetup profiles (XML), Zope page templates (TAL), `plone.app.testing`.

## Global Constraints

- Python line length 88 (black); isort `force_alphabetical_sort=True`, `multi_line_output=3`.
- FTI name: `imio.smartweb.SectionODWB`. Interface: `ISectionODWB`. Class: `SectionODWB`. Permission id: `imio.smartweb.core.CanManageSectionODWB`.
- Coexist with existing `SectionExternalContent` ODWB path — do not deprecate or migrate it.
- Reuse the existing `IOdwbViewUtils` marker interface and `odwb_widget_header` viewlet. Do NOT add a second ODS-library-loading viewlet.
- Current GS profile version is `1080`; this work bumps it to `1081`.
- Run one test: `bin/test -s imio.smartweb.core -t <name>`. Full suite: `make test`. Lint: `make lint`.
- Message factory: `from imio.smartweb.locales import SmartwebMessageFactory as _`.

## File Structure

Created:
- `src/imio/smartweb/core/contents/sections/odwb/__init__.py` — empty package marker.
- `src/imio/smartweb/core/contents/sections/odwb/content.py` — `ISectionODWB` schema + invariant, `SectionODWB` class.
- `src/imio/smartweb/core/contents/sections/odwb/view.pt` — section template wrapping markup in `ng-app`.
- `src/imio/smartweb/core/contents/sections/odwb/configure.zcml` — `browser:page` view registration.
- `src/imio/smartweb/core/profiles/default/types/imio.smartweb.SectionODWB.xml` — FTI.
- `src/imio/smartweb/core/upgrades/profiles/1080_to_1081/` — upgrade import profile (types.xml, the FTI, rolemap.xml, registry/plone.xml, page-type FTIs, icons registry).
- `src/imio/smartweb/core/tests/test_section_odwb.py` — tests.

Modified:
- `contents/__init__.py` — import `ISectionODWB`/`SectionODWB`.
- `contents/sections/configure.zcml` — `<include package=".odwb" />`.
- `permissions.zcml` — add `CanManageSectionODWB`.
- `subscribers.py` — add `_page_has_odwb_sections`, `added_odwb`, `removed_odwb`; use helper in `removed_external_content`.
- `subscribers.zcml` — register the two `ISectionODWB` subscribers.
- `profiles/default/rolemap.xml` — grant `CanManageSectionODWB`.
- `profiles/default/types.xml` — register the FTI.
- `profiles/default/types/imio.smartweb.Page.xml`, `...PortalPage.xml`, `...Procedure.xml` — add to `allowed_content_types`.
- `profiles/default/registry/plone.xml` — add to section-ordering list.
- `profiles/icons/contenttypes/registry.xml` — icon record.
- `profiles/default/metadata.xml` — version `1080` → `1081`.
- `upgrades/configure.zcml` + `profiles.zcml`/`upgrades` registration — register upgrade step 1080→1081.

---

### Task 1: Add the `CanManageSectionODWB` permission

**Files:**
- Modify: `src/imio/smartweb/core/permissions.zcml`
- Modify: `src/imio/smartweb/core/profiles/default/rolemap.xml`

**Interfaces:**
- Produces: permission id `imio.smartweb.core.CanManageSectionODWB`, title `imio.smartweb.core: Can add section ODWB`, granted to `Manager`, `Site Administrator`, `Local Manager`.

- [ ] **Step 1: Declare the permission**

In `permissions.zcml`, after the `CanManageSectionExternalContent` block, add:

```xml
  <permission
    id="imio.smartweb.core.CanManageSectionODWB"
    title="imio.smartweb.core: Can add section ODWB"
    description=""
    />
```

- [ ] **Step 2: Grant roles in rolemap**

In `profiles/default/rolemap.xml`, after the `Can add section External Content` permission block, add:

```xml
    <permission name="imio.smartweb.core: Can add section ODWB" acquire="True">
      <role name="Manager"/>
      <role name="Site Administrator"/>
      <role name="Local Manager" />
    </permission>
```

- [ ] **Step 3: Verify ZCML/XML parse**

Run: `make lint`
Expected: passes (well-formed XML). No test yet — this is plumbing consumed by Task 2.

- [ ] **Step 4: Commit**

```bash
git add src/imio/smartweb/core/permissions.zcml src/imio/smartweb/core/profiles/default/rolemap.xml
git commit -m "WEB: Add CanManageSectionODWB permission"
```

---

### Task 2: Scaffold the `SectionODWB` content type (addable, no validation yet)

**Files:**
- Create: `src/imio/smartweb/core/contents/sections/odwb/__init__.py`
- Create: `src/imio/smartweb/core/contents/sections/odwb/content.py`
- Create: `src/imio/smartweb/core/contents/sections/odwb/view.pt`
- Create: `src/imio/smartweb/core/contents/sections/odwb/configure.zcml`
- Create: `src/imio/smartweb/core/profiles/default/types/imio.smartweb.SectionODWB.xml`
- Modify: `src/imio/smartweb/core/contents/__init__.py`
- Modify: `src/imio/smartweb/core/contents/sections/configure.zcml`
- Modify: `src/imio/smartweb/core/profiles/default/types.xml`
- Modify: `src/imio/smartweb/core/profiles/default/types/imio.smartweb.Page.xml`
- Modify: `src/imio/smartweb/core/profiles/default/types/imio.smartweb.PortalPage.xml`
- Modify: `src/imio/smartweb/core/profiles/default/types/imio.smartweb.Procedure.xml`
- Modify: `src/imio/smartweb/core/profiles/default/registry/plone.xml`
- Modify: `src/imio/smartweb/core/profiles/icons/contenttypes/registry.xml`
- Test: `src/imio/smartweb/core/tests/test_section_odwb.py`

**Interfaces:**
- Produces: `ISectionODWB` (extends `ISection`), `SectionODWB(Section)`, field `odwb_widget_code: SourceText`, field `description: Text`. FTI `imio.smartweb.SectionODWB` addable in Page/PortalPage/Procedure.

- [ ] **Step 1: Invoke the plone-testing skill, then write the failing test**

Invoke `plone-testing`. Create `tests/test_section_odwb.py`:

```python
# -*- coding: utf-8 -*-

from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID


class TestSectionODWB(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    def setUp(self):
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            id="page",
        )

    def test_addable_in_page(self):
        section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionODWB",
            id="odwb",
        )
        self.assertEqual(section.portal_type, "imio.smartweb.SectionODWB")
        self.assertIn(
            "imio.smartweb.SectionODWB",
            [fti.getId() for fti in self.page.allowedContentTypes()],
        )
```

- [ ] **Step 2: Run test to verify it fails**

Run: `bin/test -s imio.smartweb.core -t TestSectionODWB.test_addable_in_page`
Expected: FAIL — `imio.smartweb.SectionODWB` type not found / not allowed.

- [ ] **Step 3: Create the package marker**

Create empty `contents/sections/odwb/__init__.py` (0 bytes, like `html/__init__.py`).

- [ ] **Step 4: Write the content schema/class**

Create `contents/sections/odwb/content.py`:

```python
# -*- coding: utf-8 -*-

from imio.smartweb.common.config import DESCRIPTION_MAX_LENGTH
from imio.smartweb.core.contents.sections.base import ISection
from imio.smartweb.core.contents.sections.base import Section
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.autoform.directives import write_permission
from zope import schema
from zope.interface import implementer


class ISectionODWB(ISection):
    """Marker interface and Dexterity Python Schema for SectionODWB"""

    write_permission(odwb_widget_code="imio.smartweb.core.CanManageSectionODWB")
    odwb_widget_code = schema.SourceText(
        title=_("ODWB widget code"),
        description=_(
            "Paste the OpenDataSoft/ODWB widget embed code here. Get it from the "
            '"Widgets" export tab of a dataset on odwb.be. The code must contain '
            "an <ods-dataset-context> widget."
        ),
        required=True,
    )

    description = schema.Text(
        title=_("Description"),
        description=_(
            "Use **text** to set text in bold. Limited to ${max} characters.",
            mapping={"max": DESCRIPTION_MAX_LENGTH},
        ),
        max_length=DESCRIPTION_MAX_LENGTH,
        required=False,
    )


@implementer(ISectionODWB)
class SectionODWB(Section):
    """SectionODWB class"""

    manage_content = True
```

- [ ] **Step 5: Write the view template**

Create `contents/sections/odwb/view.pt` (mirrors `html/view.pt`, wraps in ng-app):

```html
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
      xmlns:tal="http://xml.zope.org/namespaces/tal"
      xmlns:metal="http://xml.zope.org/namespaces/metal"
      xmlns:i18n="http://xml.zope.org/namespaces/i18n"
      lang="en"
      metal:use-macro="context/@@main_template/macros/master"
      i18n:domain="plone">
<body>

<metal:main fill-slot="content-core">
<metal:content-core define-macro="content-core">
<metal:macro use-macro="context/@@sections_macros/section_edition" />
<div class="container section-container section-odwb"
     id=""
     tal:attributes="id string:container-section-${context/id}">
    <metal:macro use-macro="context/@@sections_macros/section_title" />
    <div tal:define="collapse_klass python: 'collapse' if context.collapsible_section else ''"
         tal:attributes="class string:body-section ${collapse_klass};
                         id string:body-section-${context/id}">

      <p tal:replace="structure context/@@description" />

      <div class="odwb-widget" ng-cloak ng-app="ods-widgets">
        <div tal:content="structure context/odwb_widget_code | nothing" />
      </div>

    </div>
</div>
</metal:content-core>
</metal:main>

</body>
</html>
```

- [ ] **Step 6: Register the view**

Create `contents/sections/odwb/configure.zcml`:

```xml
<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:browser="http://namespaces.zope.org/browser">

  <browser:page
      name="view"
      for="imio.smartweb.core.contents.ISectionODWB"
      class="imio.smartweb.core.contents.sections.views.SectionView"
      template="view.pt"
      permission="zope2.View"
      layer="imio.smartweb.core.interfaces.IImioSmartwebCoreLayer"
      />

</configure>
```

- [ ] **Step 7: Include the package**

In `contents/sections/configure.zcml`, add after `<include package=".news" />` (keep alphabetical grouping is not strict here — placement after news mirrors nothing critical; add it with the other includes):

```xml
  <include package=".odwb" />
```

- [ ] **Step 8: Export the classes**

In `contents/__init__.py`, after the two `map` lines, add:

```python
from .sections.odwb.content import ISectionODWB  # NOQA
from .sections.odwb.content import SectionODWB  # NOQA
```

- [ ] **Step 9: Write the FTI**

Create `profiles/default/types/imio.smartweb.SectionODWB.xml`:

```xml
<?xml version="1.0"?>
<object xmlns:i18n="http://xml.zope.org/namespaces/i18n"
    name="imio.smartweb.SectionODWB"
    meta_type="Dexterity FTI"
    i18n:domain="imio.smartweb">

  <!-- Basic properties -->
  <property
      i18n:translate=""
      name="title">ODWB widget section</property>
  <property
      i18n:translate=""
      name="description">Section to embed an OpenDataSoft/ODWB widget</property>

  <property name="icon_expr">string:database</property>

  <!-- Hierarchy control -->
  <property name="global_allow">False</property>
  <property name="filter_content_types">True</property>
  <property name="allowed_content_types">
    <element value="Image" />
    <element value="File" />
  </property>

  <!-- Schema, class and security -->
  <property name="add_permission">imio.smartweb.core.CanManageSectionODWB</property>
  <property name="klass">imio.smartweb.core.contents.SectionODWB</property>
  <property name="schema">imio.smartweb.core.contents.ISectionODWB</property>

  <!-- Enabled behaviors -->
  <property name="behaviors" purge="false">
    <element value="plone.namefromtitle"/>
    <element value="plone.locking"/>
    <element value="plone.shortname"/>
  </property>

</object>
```

- [ ] **Step 10: Register FTI in types.xml**

In `profiles/default/types.xml`, add after the `SectionNews` line:

```xml
  <object meta_type="Dexterity FTI" name="imio.smartweb.SectionODWB"/>
```

- [ ] **Step 11: Allow in the three page types**

In each of `imio.smartweb.Page.xml`, `imio.smartweb.PortalPage.xml`, `imio.smartweb.Procedure.xml`, add inside `allowed_content_types` (keep alphabetical — after the `SectionNews` element where present, otherwise after `SectionMap`):

```xml
    <element value="imio.smartweb.SectionODWB" />
```

For `Page.xml` insert after the `SectionMap` element (Page lists no SectionNews there); for `PortalPage.xml` after `SectionNews`; for `Procedure.xml` after `SectionMap`.

- [ ] **Step 12: Add to the registry section-ordering list**

In `profiles/default/registry/plone.xml`, in the section list that begins `<element>imio.smartweb.SectionHTML</element>`, add after `<element>imio.smartweb.SectionMap</element>`:

```xml
        <element>imio.smartweb.SectionODWB</element>
```

- [ ] **Step 13: Add the icon record**

In `profiles/icons/contenttypes/registry.xml`, after the `sectionmap` record, add:

```xml
    <record name="plone.icon.contenttype/imio-smartweb-sectionodwb">
      <field type="plone.registry.field.TextLine">
        <title i18n:translate="">SectionODWB content type icon</title>
      </field>
      <value key="resource">++plone++bootstrap-icons/database.svg</value>
    </record>
```

- [ ] **Step 14: Run the test to verify it passes**

Run: `bin/test -s imio.smartweb.core -t TestSectionODWB.test_addable_in_page`
Expected: PASS.

- [ ] **Step 15: Commit**

```bash
git add src/imio/smartweb/core/contents/sections/odwb \
        src/imio/smartweb/core/contents/__init__.py \
        src/imio/smartweb/core/contents/sections/configure.zcml \
        src/imio/smartweb/core/profiles/default/types.xml \
        src/imio/smartweb/core/profiles/default/types/imio.smartweb.SectionODWB.xml \
        src/imio/smartweb/core/profiles/default/types/imio.smartweb.Page.xml \
        src/imio/smartweb/core/profiles/default/types/imio.smartweb.PortalPage.xml \
        src/imio/smartweb/core/profiles/default/types/imio.smartweb.Procedure.xml \
        src/imio/smartweb/core/profiles/default/registry/plone.xml \
        src/imio/smartweb/core/profiles/icons/contenttypes/registry.xml \
        src/imio/smartweb/core/tests/test_section_odwb.py
git commit -m "WEB: Add SectionODWB content type"
```

---

### Task 3: Structural validation (invariant)

**Files:**
- Modify: `src/imio/smartweb/core/contents/sections/odwb/content.py`
- Test: `src/imio/smartweb/core/tests/test_section_odwb.py`

**Interfaces:**
- Consumes: `ISectionODWB`, field `odwb_widget_code`.
- Produces: an `@invariant` `validate_odwb_widget_code(data)` on `ISectionODWB` that raises `zope.interface.Invalid` when `odwb_widget_code` contains no `ods-dataset-context`.

- [ ] **Step 1: Write the failing test**

Add to `tests/test_section_odwb.py`:

```python
    def test_invariant_rejects_non_ods_markup(self):
        from imio.smartweb.core.contents.sections.odwb.content import ISectionODWB
        from zope.interface import Invalid

        data = type("D", (), {"odwb_widget_code": "<p>not a widget</p>"})()
        with self.assertRaises(Invalid):
            for inv in ISectionODWB.queryTaggedValue("invariants", []):
                inv(data)

    def test_invariant_accepts_ods_markup(self):
        from imio.smartweb.core.contents.sections.odwb.content import ISectionODWB

        markup = '<ods-dataset-context context="ctx" ctx-dataset="x"></ods-dataset-context>'
        data = type("D", (), {"odwb_widget_code": markup})()
        for inv in ISectionODWB.queryTaggedValue("invariants", []):
            inv(data)  # must not raise
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `bin/test -s imio.smartweb.core -t TestSectionODWB.test_invariant_rejects_non_ods_markup`
Expected: FAIL — no invariant registered, so the loop body never raises.

- [ ] **Step 3: Add the invariant**

In `contents/sections/odwb/content.py`, add imports and the invariant. Add to imports:

```python
from zope.interface import invariant
from zope.interface import Invalid
```

Inside `class ISectionODWB(ISection):`, after the `description` field, add:

```python
    @invariant
    def validate_odwb_widget_code(data):
        code = data.odwb_widget_code or ""
        if "ods-dataset-context" not in code:
            raise Invalid(
                _(
                    "The ODWB widget code must contain an "
                    "<ods-dataset-context> widget."
                )
            )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `bin/test -s imio.smartweb.core -t TestSectionODWB.test_invariant_rejects_non_ods_markup && bin/test -s imio.smartweb.core -t TestSectionODWB.test_invariant_accepts_ods_markup`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/imio/smartweb/core/contents/sections/odwb/content.py \
        src/imio/smartweb/core/tests/test_section_odwb.py
git commit -m "WEB: Validate ODWB widget code contains ods-dataset-context"
```

---

### Task 4: Share the `IOdwbViewUtils` marker via subscribers

**Files:**
- Modify: `src/imio/smartweb/core/subscribers.py:157-176`
- Modify: `src/imio/smartweb/core/subscribers.zcml`
- Test: `src/imio/smartweb/core/tests/test_section_odwb.py`

**Interfaces:**
- Consumes: `IOdwbViewUtils` (existing), `added_external_content`/`removed_external_content` (existing at `subscribers.py`).
- Produces: `_page_has_odwb_sections(parent) -> bool`, `added_odwb(obj, event)`, `removed_odwb(obj, event)`. After this task, a page provides `IOdwbViewUtils` iff it contains ≥1 `SectionExternalContent` **or** `SectionODWB`.

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_section_odwb.py`:

```python
    def test_adding_odwb_marks_parent(self):
        from imio.smartweb.core.interfaces import IOdwbViewUtils

        self.assertFalse(IOdwbViewUtils.providedBy(self.page))
        api.content.create(
            container=self.page, type="imio.smartweb.SectionODWB", id="odwb1"
        )
        self.assertTrue(IOdwbViewUtils.providedBy(self.page))

    def test_removing_last_odwb_unmarks_parent(self):
        from imio.smartweb.core.interfaces import IOdwbViewUtils

        section = api.content.create(
            container=self.page, type="imio.smartweb.SectionODWB", id="odwb1"
        )
        api.content.delete(obj=section)
        self.assertFalse(IOdwbViewUtils.providedBy(self.page))

    def test_mixed_sections_keep_marker_until_both_gone(self):
        from imio.smartweb.core.interfaces import IOdwbViewUtils

        ext = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionExternalContent",
            id="ext",
        )
        odwb = api.content.create(
            container=self.page, type="imio.smartweb.SectionODWB", id="odwb1"
        )
        self.assertTrue(IOdwbViewUtils.providedBy(self.page))

        api.content.delete(obj=ext)
        self.assertTrue(IOdwbViewUtils.providedBy(self.page))

        api.content.delete(obj=odwb)
        self.assertFalse(IOdwbViewUtils.providedBy(self.page))
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `bin/test -s imio.smartweb.core -t TestSectionODWB.test_adding_odwb_marks_parent`
Expected: FAIL — no subscriber marks the parent.

- [ ] **Step 3: Refactor removal counting + add ODWB handlers**

In `subscribers.py`, replace the existing `removed_external_content` (currently `subscribers.py:164-176`) and add the helper + new handlers. Ensure `noLongerProvides` is imported (it is used already; if not, add `from zope.interface import noLongerProvides` and `from zope.interface import alsoProvides`). Final block:

```python
def _page_has_odwb_sections(parent):
    sections = parent.listFolderContents(
        contentFilter={
            "portal_type": [
                "imio.smartweb.SectionExternalContent",
                "imio.smartweb.SectionODWB",
            ]
        }
    )
    return len(sections) > 0


def added_external_content(obj, event):
    parent = obj.aq_parent
    if not IOdwbViewUtils.providedBy(parent):
        alsoProvides(parent, IOdwbViewUtils)
        parent.reindexObject()


def removed_external_content(obj, event):
    parent = obj.aq_parent
    if IOdwbViewUtils.providedBy(parent) and not _page_has_odwb_sections(parent):
        noLongerProvides(parent, IOdwbViewUtils)
        parent.reindexObject()


def added_odwb(obj, event):
    parent = obj.aq_parent
    if not IOdwbViewUtils.providedBy(parent):
        alsoProvides(parent, IOdwbViewUtils)
        parent.reindexObject()


def removed_odwb(obj, event):
    parent = obj.aq_parent
    if IOdwbViewUtils.providedBy(parent) and not _page_has_odwb_sections(parent):
        noLongerProvides(parent, IOdwbViewUtils)
        parent.reindexObject()
```

Note: `_page_has_odwb_sections` runs during the removed-event, at which point the object being deleted may still be listed. If the existing `test_section_external_content.py::test_parent_marker_interface` fails because the deleted object is still counted, switch the check to compare against objects other than `obj` (filter `obj` out by id). Run that existing test in Step 5 to confirm.

- [ ] **Step 4: Register the subscribers**

In `subscribers.zcml`, after the `removed_external_content` subscriber block, add:

```xml
  <subscriber for="imio.smartweb.core.contents.ISectionODWB
                   zope.lifecycleevent.interfaces.IObjectAddedEvent"
              handler=".subscribers.added_odwb" />

  <subscriber for="imio.smartweb.core.contents.ISectionODWB
                   zope.lifecycleevent.interfaces.IObjectRemovedEvent"
              handler=".subscribers.removed_odwb" />
```

- [ ] **Step 5: Run the new tests AND the existing external-content marker test**

Run: `bin/test -s imio.smartweb.core -t TestSectionODWB.test_adding_odwb_marks_parent && bin/test -s imio.smartweb.core -t TestSectionODWB.test_removing_last_odwb_unmarks_parent && bin/test -s imio.smartweb.core -t TestSectionODWB.test_mixed_sections_keep_marker_until_both_gone && bin/test -s imio.smartweb.core -t test_parent_marker_interface`
Expected: all PASS. If `test_parent_marker_interface` fails, apply the `obj`-exclusion note from Step 3 and re-run.

- [ ] **Step 6: Commit**

```bash
git add src/imio/smartweb/core/subscribers.py \
        src/imio/smartweb/core/subscribers.zcml \
        src/imio/smartweb/core/tests/test_section_odwb.py
git commit -m "WEB: Share IOdwbViewUtils marker between ODWB and external-content sections"
```

---

### Task 5: View renders markup inside the ODS ng-app wrapper

**Files:**
- Test: `src/imio/smartweb/core/tests/test_section_odwb.py`

**Interfaces:**
- Consumes: `SectionODWB`, `view.pt` (from Task 2), `SectionView`.

- [ ] **Step 1: Write the failing test**

Add to `tests/test_section_odwb.py`:

```python
    def test_view_wraps_markup_in_ng_app(self):
        from zope.component import getMultiAdapter

        markup = '<ods-dataset-context context="ctx" ctx-dataset="x"></ods-dataset-context>'
        section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionODWB",
            id="odwb1",
            odwb_widget_code=markup,
        )
        view = getMultiAdapter((section, self.request), name="view")
        html = view()
        self.assertIn('ng-app="ods-widgets"', html)
        self.assertIn("ods-dataset-context", html)
```

- [ ] **Step 2: Run test**

Run: `bin/test -s imio.smartweb.core -t TestSectionODWB.test_view_wraps_markup_in_ng_app`
Expected: PASS immediately (view.pt from Task 2 already produces this). If it FAILS on markup escaping, confirm the template uses `structure context/odwb_widget_code`.

- [ ] **Step 3: Commit**

```bash
git add src/imio/smartweb/core/tests/test_section_odwb.py
git commit -m "WEB: Test SectionODWB view renders markup in ods-widgets ng-app"
```

---

### Task 6: Upgrade step 1080 → 1081

**Files:**
- Create: `src/imio/smartweb/core/upgrades/profiles/1080_to_1081/types.xml`
- Create: `src/imio/smartweb/core/upgrades/profiles/1080_to_1081/types/imio.smartweb.SectionODWB.xml`
- Create: `src/imio/smartweb/core/upgrades/profiles/1080_to_1081/types/imio.smartweb.Page.xml`
- Create: `src/imio/smartweb/core/upgrades/profiles/1080_to_1081/types/imio.smartweb.PortalPage.xml`
- Create: `src/imio/smartweb/core/upgrades/profiles/1080_to_1081/types/imio.smartweb.Procedure.xml`
- Create: `src/imio/smartweb/core/upgrades/profiles/1080_to_1081/rolemap.xml`
- Create: `src/imio/smartweb/core/upgrades/profiles/1080_to_1081/registry/plone.xml`
- Create: `src/imio/smartweb/core/upgrades/profiles/1080_to_1081/registry.xml` (icons)
- Modify: `src/imio/smartweb/core/upgrades/configure.zcml`
- Modify: `src/imio/smartweb/core/profiles/default/metadata.xml`

**Interfaces:**
- Consumes: everything registered in Tasks 1–2.
- Produces: GS import profile `imio.smartweb.core:upgrade_1080_to_1081` that registers the new type, permission grant, allowed_content_types, registry ordering and icon on existing sites.

- [ ] **Step 1: Bump the default profile version**

In `profiles/default/metadata.xml`, change `<version>1080</version>` to `<version>1081</version>`.

- [ ] **Step 2: Create the upgrade profile GS files**

`upgrades/profiles/1080_to_1081/types.xml` — copy the current `profiles/default/types.xml` (the full `portal_types` list, now including `imio.smartweb.SectionODWB`).

`upgrades/profiles/1080_to_1081/types/imio.smartweb.SectionODWB.xml` — copy the FTI from Task 2 Step 9 verbatim.

`upgrades/profiles/1080_to_1081/types/imio.smartweb.Page.xml`, `...PortalPage.xml`, `...Procedure.xml` — copy the corresponding updated `profiles/default/types/*.xml` (with the new `allowed_content_types` element).

`upgrades/profiles/1080_to_1081/rolemap.xml` — a rolemap containing only the new permission grant:

```xml
<?xml version="1.0"?>
<rolemap>
  <permissions>
    <permission name="imio.smartweb.core: Can add section ODWB" acquire="True">
      <role name="Manager"/>
      <role name="Site Administrator"/>
      <role name="Local Manager" />
    </permission>
  </permissions>
</rolemap>
```

`upgrades/profiles/1080_to_1081/registry/plone.xml` — copy the updated `profiles/default/registry/plone.xml` (with the new section-ordering element).

`upgrades/profiles/1080_to_1081/registry.xml` — copy the updated `profiles/icons/contenttypes/registry.xml` (with the new icon record), or the single new `<record>` block wrapped in a `<registry>` root.

- [ ] **Step 3: Register the upgrade step**

In `upgrades/configure.zcml`, add the profile registration near the other `registerProfile` entries:

```xml
  <genericsetup:registerProfile
      name="upgrade_1080_to_1081"
      title="Upgrade core from 1080 to 1081"
      directory="profiles/1080_to_1081"
      description="Add SectionODWB content type, permission and registry"
      provides="Products.GenericSetup.interfaces.EXTENSION"
      />
```

And add the upgrade step at the end of the `upgradeSteps` sequence (after the 1079→1080 block):

```xml
  <genericsetup:upgradeSteps
      source="1080"
      destination="1081"
      profile="imio.smartweb.core:default">
    <genericsetup:upgradeDepends
        title="Add SectionODWB content type, permission and registry"
        import_profile="imio.smartweb.core.upgrades:upgrade_1080_to_1081"
        />
  </genericsetup:upgradeSteps>
```

- [ ] **Step 4: Verify install/reinstall is clean**

Run: `make test`
Expected: full suite PASS (the test layer applies the `default` profile at version 1081; the new type installs cleanly).

- [ ] **Step 5: Lint**

Run: `make lint`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/imio/smartweb/core/upgrades/profiles/1080_to_1081 \
        src/imio/smartweb/core/upgrades/configure.zcml \
        src/imio/smartweb/core/profiles/default/metadata.xml
git commit -m "WEB: Add upgrade step 1080 to 1081 for SectionODWB"
```

---

## Self-Review

**Spec coverage:**
- Content type `SectionODWB` → Task 2. ✓
- Permission-gated `odwb_widget_code` → Task 1 (permission) + Task 2 (`write_permission` + FTI `add_permission`). ✓
- `description` field → Task 2. ✓
- Structural validation (invariant) → Task 3. ✓
- Rendering via ng-app + shared `IOdwbViewUtils` viewlet → Task 2 (template) + Task 4 (marker). ✓
- The one existing-code touch (removal counts both types) → Task 4. ✓
- Full wiring (types.xml, allowed_content_types ×3, registry ordering, icon, rolemap) → Tasks 1–2. ✓
- Upgrade step → Task 6. ✓
- Coexist, no migration → nothing migrates existing content; old plugin untouched except shared-marker helper. ✓
- Tests incl. mixed-section removal case → Tasks 2–5. ✓

**Placeholder scan:** No TBD/TODO; all code blocks concrete. The one conditional ("if existing test fails, exclude `obj`") is a real, bounded contingency with an explicit action and verification, not a placeholder.

**Type consistency:** `_page_has_odwb_sections`, `added_odwb`, `removed_odwb` used consistently across Task 4 code and ZCML. `odwb_widget_code`, `ISectionODWB`, `SectionODWB`, `imio.smartweb.SectionODWB`, `CanManageSectionODWB` consistent across all tasks. Icon `database.svg` consistent between FTI `icon_expr` (`string:database`) and registry resource.
