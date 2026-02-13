# imio.smartweb.core

Core package for iMio SmartWeb — content types, views, behaviors, vocabularies, upgrade steps, and React webcomponents. See parent `buildout.smartweb/CLAUDE.md` for buildout-level commands and config.

## Build & test commands

```bash
make test              # Run full test suite (bin/test -s imio.smartweb.core)
make test-coverage     # Run tests with coverage (90% threshold, fail-under=90)
make run               # Start Zope instance on localhost:8080
make cleanall          # Remove venv, eggs, bin, parts — full clean rebuild
```

Run a single test:
```bash
bin/test -s imio.smartweb.core -t test_section_contact
bin/test -s imio.smartweb.core -t TestClassName.test_method_name
```

Webcomponents (from `src/imio/smartweb/core/webcomponents/`):
```bash
npm run build          # Production build (webpack --mode=production)
npm run build-dev      # Development build
npm run watch          # Dev server with hot reload (port 2000)
npm run lint           # ESLint (zero warnings tolerance)
npm run prettier       # Check formatting
```

## Code style

**Python** (setup.cfg):
- Line length: 88 (black-compatible)
- isort: `force_alphabetical_sort=True`, `multi_line_output=3`, trailing comma, parentheses
- flake8: `max-complexity=18`, ignores `W503, C812, E501, T001, C813`

**JavaScript** (webcomponents/):
- Prettier: 4-space tabs, 100 char width, trailing comma es5
- ESLint: extends `eslint:recommended` + `plugin:react/recommended`

## Architecture

### Content hierarchy

```
Folder (banner, default_page_uid)
  └── Page / PortalPage / Footer / HeroBanner / Procedure / CirkwiView
        └── Section* (16 types — see below)
```

**Section types** (all in `contents/sections/*/content.py`):
SectionText, SectionHTML, SectionLinks, SectionFiles, SectionGallery, SectionSlide, SectionVideo, SectionPostit, SectionMap, SectionCollection, SectionSelections, SectionContact, SectionEvents, SectionNews, SectionExternalContent, SectionTimestampedPublications

Base class: `Section(Container)` with fields: `hide_title`, `collapsible_section`, `background_image`, `bootstrap_css_class`, `css_class`. Properties: `manage_content`, `manage_display`, `can_toggle_title_visibility`.

### REST views (authentic sources)

Content types that display remote data from sibling iMio apps:

| Type | Authentic source | Env vars |
|------|-----------------|----------|
| `DirectoryView` | imio.directory | `DIRECTORY_URL`, `RESTAPI_DIRECTORY_CLIENT_ID/SECRET` |
| `EventsView` | imio.events | `EVENTS_URL`, `RESTAPI_EVENTS_CLIENT_ID/SECRET` |
| `NewsView` | imio.news | `NEWS_URL`, `RESTAPI_NEWS_CLIENT_ID/SECRET` |
| `CampaignView` | WCS ideabox | (WCS config) |

Request forwarders in `rest/authentic_sources.py` proxy HTTP to remote APIs with OAuth token auth.

### Behaviors (`behaviors/`)

`IOrientation`, `ICategoryDisplay`, `IImioSmartwebMinisiteSettings`, `IImioSmartwebSubsite`, `IListingBehavior`, `INewTab`, `IQuickAccess`

### Vocabularies (`vocabularies.py`)

~30 vocabularies. Key patterns:
- **Static**: `BootstrapCSSVocabulary`, `OrientationVocabulary`, `ContactBlocksVocabulary`
- **Remote (cached)**: `RemoteContactsVocabulary`, `RemoteAgendasVocabulary`, `RemoteNewsFoldersVocabulary` — use `@ram.cache` with time-based keys
- **Local**: `CurrentFolderPagesVocabulary`, `DirectoryViewsVocabulary`
- **Queryable**: `RemotePublicationsSource` (IQuerySource for AjaxSelectWidget)

### Upgrade steps (`upgrades/`)

Pattern — stateless functions registered in GenericSetup ZCML:
```python
def my_upgrade(context):
    portal = api.portal.get()
    brains = api.content.find(portal_type="imio.smartweb.Page")
    for brain in brains:
        obj = brain.getObject()
        # migrate data
        obj.reindexObject(idxs=["relevant_index"])
```
Use `api.env.adopt_user(username="admin")` when elevated permissions are needed.

## Testing

### Layers and base class (`testing.py`)

```python
IMIO_SMARTWEB_CORE_INTEGRATION_TESTING  # Most tests use this
IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING   # Browser-like tests
IMIO_SMARTWEB_CORE_ACCEPTANCE_TESTING   # Robot Framework
```

Base class: `ImioSmartwebTestCase(unittest.TestCase)` — provides `assertVocabularyLen()`.

Layer setup mocks HTTP requests to directory/events/news entities via `requests_mock` and creates a test user with Site Administrator role.

### Test environment variables (test_plone6.cfg)

```
zope_i18n_compile_mo_files = true
TZ = UTC
DIRECTORY_URL = http://localhost:8080/Plone
EVENTS_URL = http://localhost:8080/Plone
NEWS_URL = http://localhost:8080/Plone
```

### Writing tests

```python
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone.app.testing import setRoles, TEST_USER_ID
import requests_mock

class TestFeature(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    @requests_mock.Mocker()
    def test_remote_data(self, m):
        m.get("http://localhost:8080/Plone/@search", json=mock_data)
        # assertions
```

### Mock resources (`tests/resources/`)

JSON fixtures: `json_contact_raw_mock.json`, `json_events_agendas_raw_mock.json`, `json_directory_entities_raw_mock.json`, etc.

Utilities in `tests/utils.py`: `get_json()`, `get_html()`, `get_sections_types()`, `make_named_image()`, `clear_cache()`, `FakeResponse`.

## WebComponents

React 18 + Webpack 5 app in `src/imio/smartweb/core/webcomponents/`. Single entry point (`src/index.jsx`) builds **5 custom HTML elements**:

| Element | Component | Purpose |
|---------|-----------|---------|
| `<smartweb-annuaire>` | Annuaire | Directory/contact listings with map |
| `<smartweb-events>` | Events | Event listings with date filtering |
| `<smartweb-news>` | News | News article listings |
| `<smartweb-search>` | Search | Unified multi-content search |
| `<smartweb-campaign>` | Campaign | Campaign/project listings with map |

Each component follows the same structure: main component, Card, Content, List sub-components, and Filter.

Output: `build/js/smartweb-webcomponents-compiled.js` + code-split chunks.

Key deps: React Router DOM, React Bootstrap, Leaflet/React-Leaflet (maps), Axios, React-Select, React-DatePicker, date-fns.
