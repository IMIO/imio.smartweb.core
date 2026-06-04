# -*- coding: utf-8 -*-

from plone import api
from plone.app.textfield.value import RichTextValue
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five.browser import BrowserView
from urllib.parse import urlparse
from zope.interface import alsoProvides

import re

from lxml import html as lxml_html

_SEARCHED_STRING = "/fr/"

_KEYWORDS = ["www.liege.be", "Plone", "annuaire", "preprod"]


def _extract_urls(html_string):
    """Extract all (attribute, value) pairs for href (<a>) and src attributes
    from an HTML string."""
    if not html_string:
        return []
    try:
        doc = lxml_html.fromstring(html_string)
    except Exception:
        return []
    results = []
    for href in doc.xpath("//a/@href"):
        results.append(("href", href))
    for src in doc.xpath("//*/@src"):
        results.append(("src", src))
    return results


def _fix_url(url):
    """Compute the corrected URL: every matched URL becomes a root-relative
    path on the new site (scheme and domain are dropped — the content was
    migrated) and the "/fr" path part is removed.

    Handles the malformed URLs found in migrated content:
    - doubled scheme: http://https://www.liege.be/fr/x → /x
    - "fr" taken for a domain: http://fr/annuaire/x?u=1 → /annuaire/x?u=1
    - hardcoded instance: http://localhost:8080/Plone/fr/x → /x
    """
    new_url = url
    # drop doubled scheme (e.g. "http://https://…")
    new_url = re.sub(r"^https?://(?=https?://)", "", new_url)
    parsed = urlparse(new_url)
    path = parsed.path or "/"
    # drop the hardcoded /Plone site prefix
    if path == "/Plone":
        path = "/"
    elif path.startswith("/Plone/"):
        path = path[len("/Plone") :]
    # remove the "/fr" path part
    path = path.replace("/fr/", "/")
    if path.endswith("/fr"):
        path = path[: -len("/fr")] or "/"
    if not path.startswith("/"):
        path = "/" + path
    if parsed.query:
        path += "?" + parsed.query
    if parsed.fragment:
        path += "#" + parsed.fragment
    return path


def _replace_in_html(html, old_url, new_url):
    """Replace a URL in an HTML string, including its &amp;-escaped form
    (lxml unescapes entities when extracting attribute values)."""
    result = html.replace(old_url, new_url)
    escaped_old = old_url.replace("&", "&amp;")
    if escaped_old != old_url:
        result = result.replace(escaped_old, new_url.replace("&", "&amp;"))
    return result


class FindFrUrlsView(BrowserView):
    """Browse all SectionText and SectionHTML objects and report every URL
    (href or src attribute) containing the string "/fr/" and at least one
    keyword. In dry-run mode (default) only a report is displayed; with
    ?apply=1 the corrected URLs are written back into the contents."""

    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        self.matches = []
        self.apply = bool(self.request.form.get("apply"))

        self._scan_section_text()
        self._scan_section_html()

        return self.index()

    # ------------------------------------------------------------------
    # Scanners per content type
    # ------------------------------------------------------------------

    def _scan_section_text(self):
        """Parse rich text (plone.richtext behaviour) stored in SectionText."""
        for brain in api.content.find(portal_type="imio.smartweb.SectionText"):
            obj = brain.getObject()
            richtext = getattr(obj, "text", None)
            if richtext is None:
                continue
            # raw is the stored source we can modify; fall back to output
            html = (
                getattr(richtext, "raw", None)
                or getattr(richtext, "output", None)
                or ""
            )
            replacements = self._check_urls(obj, html)
            if self.apply and replacements:
                new_html = html
                for old_url, new_url in replacements:
                    new_html = _replace_in_html(new_html, old_url, new_url)
                if new_html != html:
                    obj.text = RichTextValue(
                        new_html,
                        mimeType=richtext.mimeType,
                        outputMimeType=richtext.outputMimeType,
                        encoding=richtext.encoding,
                    )
                    obj.reindexObject()

    def _scan_section_html(self):
        """Parse the raw HTML field stored in SectionHTML."""
        for brain in api.content.find(portal_type="imio.smartweb.SectionHTML"):
            obj = brain.getObject()
            html = getattr(obj, "html", None) or ""
            replacements = self._check_urls(obj, html)
            if self.apply and replacements:
                new_html = html
                for old_url, new_url in replacements:
                    new_html = _replace_in_html(new_html, old_url, new_url)
                if new_html != html:
                    obj.html = new_html
                    obj.reindexObject()

    # ------------------------------------------------------------------
    # URL matching
    # ------------------------------------------------------------------

    def _check_urls(self, obj, html):
        """Record matching URLs in self.matches and return the list of
        (old_url, new_url) replacements to apply on this object."""
        replacements = []
        for attribute, url in _extract_urls(html):
            if _SEARCHED_STRING not in url:
                continue
            keywords = [keyword for keyword in _KEYWORDS if keyword in url]
            if not keywords:
                continue
            fixed_url = _fix_url(url)
            replacements.append((url, fixed_url))
            self.matches.append(
                {
                    "object_url": obj.absolute_url(),
                    "portal_type": obj.portal_type,
                    "link_url": url,
                    "fixed_url": fixed_url,
                    "attribute": attribute,
                    "keywords": ", ".join(keywords),
                }
            )
        return replacements
