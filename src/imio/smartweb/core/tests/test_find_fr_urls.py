# -*- coding: utf-8 -*-

from imio.smartweb.core.browser.migration.find_fr_urls import _extract_urls
from imio.smartweb.core.browser.migration.find_fr_urls import _fix_url
from imio.smartweb.core.browser.migration.find_fr_urls import _replace_in_html
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.textfield.value import RichTextValue


class TestFindFrUrls(ImioSmartwebTestCase):
    """Module-level helper functions of find_fr_urls.py."""

    def test_extract_urls(self):
        html = (
            '<div><a href="https://example.org/a">link</a>'
            '<img src="/images/photo.jpg" />'
            '<iframe src="https://example.org/embed"></iframe>'
            "<p>no url here</p></div>"
        )
        self.assertEqual(
            _extract_urls(html),
            [
                ("href", "https://example.org/a"),
                ("src", "/images/photo.jpg"),
                ("src", "https://example.org/embed"),
            ],
        )
        self.assertEqual(_extract_urls(""), [])
        self.assertEqual(_extract_urls(None), [])

    def test_fix_url(self):
        cases = [
            # hardcoded instance URL
            (
                "http://localhost:8080/Plone/fr/vie-communale/services",
                "/vie-communale/services",
            ),
            ("http://localhost:8080/Plone/fr", "/"),
            ("http://localhost:8080/Plone", "/"),
            # www.liege.be
            ("https://www.liege.be/fr/ma-page", "/ma-page"),
            ("https://www.liege.be/fr/", "/"),
            ("https://www.liege.be/fr", "/"),
            ("https://www.liege.be/fr/services?x=1#anchor", "/services?x=1#anchor"),
            # "fr" taken for a domain during migration
            ("http://fr/annuaire/abeva?u=730e5590", "/annuaire/abeva?u=730e5590"),
            ("https://fr/annuaire/vivaqua?u=f7d2", "/annuaire/vivaqua?u=f7d2"),
            # doubled scheme
            ("http://https://www.liege.be/fr/proprete/actu", "/proprete/actu"),
            # already relative
            (
                "/fr/annuaire#c11=faceted-preview-contacts&b_start=0",
                "/annuaire#c11=faceted-preview-contacts&b_start=0",
            ),
            # preprod
            ("https://liege-preprod.imio.be/fr/page", "/page"),
        ]
        for url, expected in cases:
            self.assertEqual(_fix_url(url), expected, url)

    def test_replace_in_html(self):
        html = '<a href="https://www.liege.be/fr/page">x</a>'
        self.assertEqual(
            _replace_in_html(html, "https://www.liege.be/fr/page", "/page"),
            '<a href="/page">x</a>',
        )
        # lxml unescapes entities when extracting attribute values: the URL
        # stored as &amp; in the HTML source must be replaced too.
        html = '<a href="/fr/page?a=1&amp;b=2">x</a>'
        self.assertEqual(
            _replace_in_html(html, "/fr/page?a=1&b=2", "/page?a=1&b=2"),
            '<a href="/page?a=1&amp;b=2">x</a>',
        )


class TestFindFrUrlsView(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.request.form.pop("apply", None)
        self.page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="Page",
        )

    def _render(self):
        view = api.content.get_view(
            name="find_fr_urls",
            context=self.portal,
            request=self.request,
        )
        html = view()
        return view, html

    def test_call(self):
        section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionText",
            title="Section text",
        )
        section.text = RichTextValue(
            '<p><a href="https://www.liege.be/fr/ma-page">lien</a></p>',
            "text/html",
            "text/html",
        )
        # dry-run by default: report only, banner, nothing modified
        view, html = self._render()
        self.assertFalse(view.apply)
        self.assertIn("dry-run", html)
        self.assertIn("https://www.liege.be/fr/ma-page", html)
        self.assertIn("/ma-page", html)
        self.assertIn("www.liege.be", html)
        self.assertIn("/fr/ma-page", section.text.raw)
        # ?apply=1 switches to apply mode
        self.request.form["apply"] = "1"
        view, html = self._render()
        self.assertTrue(view.apply)
        self.assertNotIn("dry-run", html)

    def test_scan_section_text(self):
        section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionText",
            title="Section text",
        )
        section.text = RichTextValue(
            '<p><a href="http://localhost:8080/Plone/fr/vie-communale">a</a>'
            '<a href="https://www.liege.be/fr/services?x=1">b</a></p>',
            "text/html",
            "text/html",
        )
        # a section without text must be skipped without error
        api.content.create(
            container=self.page,
            type="imio.smartweb.SectionText",
            title="Empty section",
        )
        self.request.form["apply"] = "1"
        view, html = self._render()
        self.assertEqual(len(view.matches), 2)
        self.assertEqual(
            section.text.raw,
            '<p><a href="/vie-communale">a</a><a href="/services?x=1">b</a></p>',
        )
        # mimetype is preserved when the RichTextValue is rewritten
        self.assertEqual(section.text.mimeType, "text/html")

    def test_scan_section_html(self):
        section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionHTML",
            title="Section html",
            html='<div><a href="http://fr/annuaire/abeva?u=1">a</a></div>',
        )
        self.request.form["apply"] = "1"
        view, html = self._render()
        self.assertEqual(len(view.matches), 1)
        self.assertEqual(
            section.html,
            '<div><a href="/annuaire/abeva?u=1">a</a></div>',
        )

    def test_check_urls(self):
        section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionHTML",
            title="Section html",
            html=(
                # matches: /fr/ + keywords www.liege.be
                '<a href="https://www.liege.be/fr/page">kept</a>'
                # ignored: /fr/ but no keyword
                '<a href="https://example.org/fr/page">no-keyword</a>'
                # ignored: keyword but no /fr/
                '<a href="https://www.liege.be/nl/page">no-fr</a>'
                # matches: src attribute, two keywords (Plone + preprod)
                '<img src="http://preprod.imio.be/Plone/fr/image.jpg" />'
            ),
        )
        view, html = self._render()
        self.assertEqual(len(view.matches), 2)
        first, second = view.matches
        self.assertEqual(first["object_url"], section.absolute_url())
        self.assertEqual(first["portal_type"], "imio.smartweb.SectionHTML")
        self.assertEqual(first["link_url"], "https://www.liege.be/fr/page")
        self.assertEqual(first["fixed_url"], "/page")
        self.assertEqual(first["attribute"], "href")
        self.assertEqual(first["keywords"], "www.liege.be")
        self.assertEqual(
            second["link_url"], "http://preprod.imio.be/Plone/fr/image.jpg"
        )
        self.assertEqual(second["fixed_url"], "/image.jpg")
        self.assertEqual(second["attribute"], "src")
        self.assertEqual(second["keywords"], "Plone, preprod")
        # dry-run: nothing was modified
        self.assertIn("https://www.liege.be/fr/page", section.html)


# <audit>
#   <file>test_find_fr_urls.py</file>
#   <requirements_applied>R1, R2, R5, R6</requirements_applied>
#   <deviations>None</deviations>
#   <questions>None</questions>
# </audit>
