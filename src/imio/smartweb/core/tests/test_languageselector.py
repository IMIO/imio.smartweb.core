# -*- coding: utf-8 -*-

from imio.smartweb.core.interfaces import IImioSmartwebCoreLayer
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.i18n.interfaces import ILanguageSchema
from plone.registry.interfaces import IRegistry
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import alsoProvides
from zope.viewlet.interfaces import IViewlet
from zope.viewlet.interfaces import IViewletManager


class TestLanguageSelector(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        alsoProvides(self.request, IImioSmartwebCoreLayer)
        # Make the site multilingual so the language selector is available.
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ILanguageSchema, prefix="plone")
        settings.available_languages = ["fr", "nl"]
        settings.default_language = "fr"
        settings.use_cookie_negotiation = True

    def enable_dropdown(self, enabled):
        api.portal.set_registry_record("smartweb.language_selector_dropdown", enabled)

    def render_selector(self):
        view = self.portal.restrictedTraverse("@@plone")
        manager = getMultiAdapter(
            (self.portal, self.request, view),
            IViewletManager,
            name="imio.smartweb.header_actions_viewletmanager",
        )
        viewlet = getMultiAdapter(
            (self.portal, self.request, view, manager),
            IViewlet,
            name="plone.app.multilingual.languageselector",
        )
        viewlet.update()
        return viewlet.render()

    def test_classic_selector_by_default(self):
        # The dropdown is opt-in: without the setting, the classic flat list
        # (languages side by side) is kept.
        self.assertFalse(
            api.portal.get_registry_record("smartweb.language_selector_dropdown")
        )
        html = self.render_selector()
        self.assertIn('id="portal-languageselector"', html)
        self.assertIn("<ul", html)
        self.assertNotIn("dropdown-toggle", html)
        self.assertNotIn("dropdown-menu", html)
        self.assertIn("currentLanguage", html)
        self.assertIn("Français", html)
        self.assertIn("Nederlands", html)

    def test_renders_bootstrap_dropdown_when_enabled(self):
        self.enable_dropdown(True)
        html = self.render_selector()
        self.assertIn('id="portal-languageselector"', html)
        self.assertIn("dropdown-toggle", html)
        self.assertIn("dropdown-menu", html)
        self.assertIn('data-bs-toggle="dropdown"', html)
        self.assertIn('aria-expanded="false"', html)

    def test_current_language_is_the_toggle(self):
        self.enable_dropdown(True)
        html = self.render_selector()
        # The current language (default "fr") drives the toggle button...
        self.assertIn("currentLanguage", html)
        toggle = html[html.index("dropdown-toggle") : html.index("dropdown-menu")]
        self.assertIn("Français", toggle)
        # ...and is NOT repeated as a menu item.
        menu = html[html.index("dropdown-menu") :]
        self.assertNotIn("dropdown-item", toggle)
        self.assertNotIn("Français", menu)

    def test_other_languages_are_dropdown_items(self):
        self.enable_dropdown(True)
        html = self.render_selector()
        menu = html[html.index("dropdown-menu") :]
        self.assertIn("dropdown-item", menu)
        self.assertIn("Nederlands", menu)
        self.assertIn("@@multilingual-selector/", menu)
        self.assertIn("/nl", menu)

    def test_names_shown_when_flags_disabled(self):
        # Flags are an optional Plone feature, disabled by default: the selector
        # must fall back to language names, both in the toggle and the items.
        self.enable_dropdown(True)
        html = self.render_selector()
        self.assertIn("Français", html)
        self.assertIn("Nederlands", html)
        self.assertNotIn("plone-icon-flag", html)


# <audit>
#   <file>test_languageselector.py</file>
#   <requirements_applied>R1, R2, R3, R5, R6</requirements_applied>
#   <deviations>
#     R2: no ready-made "trigger action" — the selector renders from the site's
#     language configuration and a control panel setting, so setUp configures a
#     real multilingual site (registry ILanguageSchema, no mocking) and each
#     test flips the real 'smartweb.language_selector_dropdown' registry record
#     then renders the real viewlet through the component registry, asserting
#     the observable HTML (classic list vs Bootstrap dropdown).
#   </deviations>
#   <questions>None</questions>
# </audit>
