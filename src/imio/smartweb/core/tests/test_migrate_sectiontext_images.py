# -*- coding: utf-8 -*-

from imio.smartweb.core.browser.migration.migrate_sectiontext_images import (
    _classify_src,
)
from imio.smartweb.core.browser.migration.migrate_sectiontext_images import (
    _download_external_image,
)
from imio.smartweb.core.browser.migration.migrate_sectiontext_images import (
    _extract_attr,
)
from imio.smartweb.core.browser.migration.migrate_sectiontext_images import (
    _filename_from_url,
)
from imio.smartweb.core.browser.migration.migrate_sectiontext_images import (
    _iter_img_tags,
)
from imio.smartweb.core.browser.migration.migrate_sectiontext_images import (
    _resolve_uid_image,
)
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import make_named_image
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.textfield.value import RichTextValue
from plone.folder.interfaces import IExplicitOrdering
from unittest import mock

import requests_mock


class TestMigrateSectionTextImagesHelpers(ImioSmartwebTestCase):
    """Module-level helper functions (no Plone content needed)."""

    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def test_iter_img_tags(self):
        raw = (
            '<p>Texte <img src="resolveuid/abc" alt="x" /> suite</p>'
            '<p><img src="http://ex.org/a.png"></p>'
        )
        tags = _iter_img_tags(raw)
        self.assertEqual(len(tags), 2)
        self.assertIn('src="resolveuid/abc"', tags[0])
        self.assertIn('src="http://ex.org/a.png"', tags[1])
        self.assertEqual(_iter_img_tags(""), [])
        self.assertEqual(_iter_img_tags(None), [])
        self.assertEqual(_iter_img_tags("<p>text</p>"), [])

    def test_extract_attr(self):
        tag = '<img src="resolveuid/abc" alt="Mon image" />'
        self.assertEqual(_extract_attr(tag, "src"), "resolveuid/abc")
        self.assertEqual(_extract_attr(tag, "alt"), "Mon image")
        self.assertEqual(_extract_attr(tag, "title"), "")
        # single quotes are supported too
        self.assertEqual(_extract_attr("<img src='a.png'>", "src"), "a.png")

    def test_extract_attr_ignores_data_prefix(self):
        tag = '<img data-src="trap.png" src="real.png">'
        self.assertEqual(_extract_attr(tag, "src"), "real.png")

    def test_classify_src(self):
        portal = "http://localhost:8080/Plone"
        self.assertEqual(
            _classify_src("resolveuid/abc123", portal), ("resolveuid", "abc123")
        )
        self.assertEqual(
            _classify_src("../resolveuid/xyz/@@images/image", portal),
            ("resolveuid", "xyz"),
        )
        self.assertEqual(
            _classify_src("https://ex.org/a.png", portal),
            ("external", "https://ex.org/a.png"),
        )
        # same portal -> unsupported (kept in place)
        self.assertEqual(
            _classify_src(portal + "/image/@@images/image", portal)[0],
            "unsupported",
        )
        self.assertEqual(
            _classify_src("data:image/png;base64,AAAA", portal)[0], "unsupported"
        )
        self.assertEqual(_classify_src("/relative/path.png", portal)[0], "unsupported")
        self.assertEqual(_classify_src("", portal)[0], "unsupported")

    def test_iter_img_tags_handles_gt_in_attribute(self):
        raw = '<p><img src="https://ex.org/a.png" alt="grand > petit" /></p>'
        tags = _iter_img_tags(raw)
        self.assertEqual(len(tags), 1)
        self.assertIn('alt="grand > petit"', tags[0])


class TestMigrateSectionTextImagesIntegration(ImioSmartwebTestCase):
    """Integration tests needing Plone content."""

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

    def test_resolve_uid_image(self):
        gallery = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionGallery",
            title="Gallery",
        )
        image = api.content.create(container=gallery, type="Image", title="plone.png")
        uid = image.UID()
        self.assertEqual(_resolve_uid_image(uid), image)
        # unknown uid -> None
        self.assertIsNone(_resolve_uid_image("does-not-exist"))
        # existing object that is NOT an Image -> None
        self.assertIsNone(_resolve_uid_image(self.page.UID()))

    def test_filename_from_url(self):
        self.assertEqual(
            _filename_from_url("https://ex.org/path/photo.jpg"), "photo.jpg"
        )
        self.assertEqual(
            _filename_from_url("https://ex.org/path/mon%20image.png"),
            "mon image.png",
        )
        self.assertEqual(_filename_from_url("https://ex.org/"), "image")

    @requests_mock.Mocker()
    def test_download_external_image_ok(self, m):
        data = make_named_image("plone.png")["data"]
        url = "https://ex.org/photo.png"
        m.get(url, content=data, headers={"Content-Type": "image/png"})
        cache = {}
        got_data, filename, content_type, error = _download_external_image(url, cache)
        self.assertEqual(got_data, data)
        self.assertEqual(filename, "photo.png")
        self.assertEqual(content_type, "image/png")
        self.assertIsNone(error)
        # second call is served from cache (no new request needed)
        self.assertIn(url, cache)

    @requests_mock.Mocker()
    def test_download_external_image_http_error(self, m):
        url = "https://ex.org/missing.png"
        m.get(url, status_code=404)
        data, filename, content_type, error = _download_external_image(url, {})
        self.assertIsNone(data)
        self.assertEqual(error, "HTTP 404")

    @requests_mock.Mocker()
    def test_download_external_image_timeout(self, m):
        import requests as rq

        url = "https://ex.org/slow.png"
        m.get(url, exc=rq.exceptions.Timeout)
        _, _, _, error = _download_external_image(url, {})
        self.assertEqual(error, "Timeout")

    @requests_mock.Mocker()
    def test_download_external_image_connection_error(self, m):
        import requests as rq

        url = "https://ex.org/unreachable.png"
        m.get(url, exc=rq.exceptions.ConnectionError("refused"))
        _, _, _, error = _download_external_image(url, {})
        self.assertIn("Connection error", error)

    def _render(self):
        view = api.content.get_view(
            name="migrate_sectiontext_images",
            context=self.portal,
            request=self.request,
        )
        html = view()
        return view, html

    def test_view_renders_dry_run(self):
        view, html = self._render()
        self.assertFalse(view.apply)
        self.assertIn("dry-run", html)
        self.assertEqual(view.results, [])

    def test_view_apply_flag(self):
        self.request.form["apply"] = "1"
        view, html = self._render()
        self.assertTrue(view.apply)
        self.assertNotIn("dry-run", html)

    # ------------------------------------------------------------------
    # Task 6: _process_section — detection and report (dry-run, no writes)
    # ------------------------------------------------------------------

    def _make_section(self, raw, title="Section text"):
        section = api.content.create(
            container=self.page, type="imio.smartweb.SectionText", title=title
        )
        section.text = RichTextValue(raw, "text/html", "text/html")
        return section

    def test_process_dry_run_classifies_without_writing(self):
        # Image must be in self.portal (Page FTI does not allow Image children)
        image = api.content.create(
            container=self.portal, type="Image", title="plone.png"
        )
        raw = (
            '<p><img src="resolveuid/%s" alt="Photo" />'
            '<img src="https://ex.org/a.png" />'
            '<img src="data:image/png;base64,AAAA" /></p>' % image.UID()
        )
        section = self._make_section(raw)
        view, html = self._render()
        # nothing written in dry-run
        self.assertEqual(section.text.raw, raw)
        self.assertEqual(
            len(
                [
                    o
                    for o in self.page.objectValues()
                    if o.portal_type == "imio.smartweb.SectionGallery"
                ]
            ),
            0,
        )
        # one report entry with three classified images
        self.assertEqual(len(view.results), 1)
        statuses = [img["status"] for img in view.results[0]["images"]]
        self.assertEqual(statuses.count("to_migrate"), 2)  # resolveuid + external
        self.assertEqual(statuses.count("skipped"), 1)  # data-uri

    def test_process_skips_section_without_img(self):
        self._make_section("<p>Pas d'image ici</p>")
        view, html = self._render()
        self.assertEqual(view.results, [])

    def test_process_reports_missing_resolveuid_as_failed(self):
        self._make_section('<p><img src="resolveuid/nope" /></p>')
        view, html = self._render()
        self.assertEqual(view.results[0]["images"][0]["status"], "failed")

    # ------------------------------------------------------------------
    # Task 7: _apply_section — gallery + resolveuid copy + positioning
    # ------------------------------------------------------------------

    def test_apply_resolveuid_creates_gallery_after_section(self):
        # Image must be outside self.page to keep gallery count == 1
        image = api.content.create(
            container=self.portal, type="Image", title="plone.png"
        )
        section = self._make_section(
            '<p>Avant <img src="resolveuid/%s" alt="Photo" /> après</p>' % image.UID()
        )
        self.request.form["apply"] = "1"
        view, html = self._render()

        # a gallery was created in the page
        galleries = [
            o
            for o in self.page.objectValues()
            if o.portal_type == "imio.smartweb.SectionGallery"
        ]
        self.assertEqual(len(galleries), 1)
        gallery = galleries[0]
        # it contains a copy of the Image
        gallery_images = [o for o in gallery.objectValues() if o.portal_type == "Image"]
        self.assertEqual(len(gallery_images), 1)
        # the gallery sits immediately after the SectionText
        ordering = IExplicitOrdering(self.page)
        self.assertEqual(
            ordering.getObjectPosition(gallery.getId()),
            ordering.getObjectPosition(section.getId()) + 1,
        )
        # the <img> was stripped from the rich text, surrounding text kept
        self.assertNotIn("<img", section.text.raw)
        self.assertIn("Avant", section.text.raw)
        self.assertIn("après", section.text.raw)
        # mimetype preserved
        self.assertEqual(section.text.mimeType, "text/html")
        # report marks it migrated
        self.assertEqual(view.results[0]["images"][0]["status"], "migrated")
        self.assertTrue(view.results[0]["gallery_created"])

    # ------------------------------------------------------------------
    # Task 8: _apply_section — external image downloaded into gallery
    # ------------------------------------------------------------------

    @requests_mock.Mocker()
    def test_apply_external_downloads_into_gallery(self, m):
        data = make_named_image("plone.png")["data"]
        url = "https://ex.org/photo.png"
        m.get(url, content=data, headers={"Content-Type": "image/png"})
        section = self._make_section('<p><img src="%s" alt="Externe" /></p>' % url)
        self.request.form["apply"] = "1"
        view, html = self._render()

        galleries = [
            o
            for o in self.page.objectValues()
            if o.portal_type == "imio.smartweb.SectionGallery"
        ]
        self.assertEqual(len(galleries), 1)
        gallery_images = [
            o for o in galleries[0].objectValues() if o.portal_type == "Image"
        ]
        self.assertEqual(len(gallery_images), 1)
        self.assertEqual(gallery_images[0].title, "Externe")
        self.assertEqual(gallery_images[0].image.data, data)
        self.assertNotIn("<img", section.text.raw)
        self.assertEqual(view.results[0]["images"][0]["status"], "migrated")

    @requests_mock.Mocker()
    def test_apply_external_failure_keeps_img(self, m):
        url = "https://ex.org/missing.png"
        m.get(url, status_code=404)
        section = self._make_section('<p><img src="%s" /></p>' % url)
        self.request.form["apply"] = "1"
        view, html = self._render()
        # download failed: img kept, NO gallery created (lazy creation)
        self.assertIn("<img", section.text.raw)
        self.assertEqual(view.results[0]["images"][0]["status"], "failed")
        self.assertEqual(view.results[0]["images"][0]["reason"], "HTTP 404")
        self.assertFalse(view.results[0]["gallery_created"])
        galleries = [
            o
            for o in self.page.objectValues()
            if o.portal_type == "imio.smartweb.SectionGallery"
        ]
        self.assertEqual(len(galleries), 0)

    # ------------------------------------------------------------------
    # Task 9: Edge cases — unsupported kept & idempotence
    # ------------------------------------------------------------------

    def test_apply_unsupported_kept_no_gallery(self):
        section = self._make_section('<p><img src="data:image/png;base64,AAAA" /></p>')
        self.request.form["apply"] = "1"
        view, html = self._render()
        self.assertIn("<img", section.text.raw)
        self.assertEqual(view.results[0]["images"][0]["status"], "skipped")
        # no migratable image -> no gallery created
        self.assertFalse(view.results[0]["gallery_created"])
        self.assertEqual(
            len(
                [
                    o
                    for o in self.page.objectValues()
                    if o.portal_type == "imio.smartweb.SectionGallery"
                ]
            ),
            0,
        )

    def test_apply_is_idempotent(self):
        image = api.content.create(
            container=self.portal, type="Image", title="plone.png"
        )
        self._make_section('<p><img src="resolveuid/%s" /></p>' % image.UID())
        self.request.form["apply"] = "1"
        self._render()  # first apply
        self._render()  # second apply must not create a second gallery
        galleries = [
            o
            for o in self.page.objectValues()
            if o.portal_type == "imio.smartweb.SectionGallery"
        ]
        self.assertEqual(len(galleries), 1)

    @requests_mock.Mocker()
    def test_apply_mixed_success_and_failure(self, m):
        url = "https://ex.org/missing.png"
        m.get(url, status_code=404)
        image = api.content.create(
            container=self.portal, type="Image", title="plone.png"
        )
        section = self._make_section(
            '<p><img src="resolveuid/%s" alt="ok" />'
            '<img src="%s" /></p>' % (image.UID(), url)
        )
        self.request.form["apply"] = "1"
        view, html = self._render()
        galleries = [
            o
            for o in self.page.objectValues()
            if o.portal_type == "imio.smartweb.SectionGallery"
        ]
        self.assertEqual(len(galleries), 1)
        gallery_images = [
            o for o in galleries[0].objectValues() if o.portal_type == "Image"
        ]
        self.assertEqual(len(gallery_images), 1)
        self.assertNotIn("resolveuid", section.text.raw)
        self.assertIn(url, section.text.raw)
        statuses = sorted(img["status"] for img in view.results[0]["images"])
        self.assertEqual(statuses, ["failed", "migrated"])

    def test_position_after_with_preceding_section(self):
        api.content.create(
            container=self.page,
            type="imio.smartweb.SectionText",
            title="Before",
        )
        image = api.content.create(
            container=self.portal, type="Image", title="plone.png"
        )
        section = self._make_section(
            '<p><img src="resolveuid/%s" /></p>' % image.UID(), title="Target"
        )
        self.request.form["apply"] = "1"
        self._render()
        gallery = [
            o
            for o in self.page.objectValues()
            if o.portal_type == "imio.smartweb.SectionGallery"
        ][0]
        ordering = IExplicitOrdering(self.page)
        self.assertEqual(
            ordering.getObjectPosition(gallery.getId()),
            ordering.getObjectPosition(section.getId()) + 1,
        )

    def test_apply_duplicate_identical_imgs(self):
        image = api.content.create(
            container=self.portal, type="Image", title="plone.png"
        )
        tag = '<img src="resolveuid/%s" />' % image.UID()
        section = self._make_section("<p>%s%s</p>" % (tag, tag))
        self.request.form["apply"] = "1"
        self._render()
        self.assertNotIn("<img", section.text.raw)
        gallery = [
            o
            for o in self.page.objectValues()
            if o.portal_type == "imio.smartweb.SectionGallery"
        ][0]
        gallery_images = [o for o in gallery.objectValues() if o.portal_type == "Image"]
        self.assertEqual(len(gallery_images), 2)

    @requests_mock.Mocker()
    def test_apply_external_with_gt_in_alt_is_clean(self, m):
        data = make_named_image("plone.png")["data"]
        url = "https://ex.org/photo.png"
        m.get(url, content=data, headers={"Content-Type": "image/png"})
        section = self._make_section(
            '<p><img src="%s" alt="grand > petit" /></p>' % url
        )
        self.request.form["apply"] = "1"
        self._render()
        # the whole tag (incl. the > inside alt) was removed cleanly
        self.assertNotIn("<img", section.text.raw)
        self.assertNotIn("petit", section.text.raw)

    # ------------------------------------------------------------------
    # Task 10: Full report template — summary + per-section detail
    # ------------------------------------------------------------------

    def test_report_shows_summary_and_detail(self):
        image = api.content.create(
            container=self.portal, type="Image", title="plone.png"
        )
        self._make_section(
            '<p><img src="resolveuid/%s" alt="Photo" /></p>' % image.UID(),
            title="Ma section",
        )
        view, html = self._render()  # dry-run
        # summary numbers and detail are rendered
        self.assertIn("SectionText concernées", html)
        self.assertIn("Ma section", html)  # gallery title contains it
        self.assertIn("resolveuid", html)  # image source / type
        self.assertIn("to_migrate", html)  # status shown

    # ------------------------------------------------------------------
    # Hardening: data-safety branches (savepoint rollback, position
    # fallback) and the SSL download-error branch.
    # ------------------------------------------------------------------

    def test_apply_section_rolls_back_on_write_failure(self):
        # A failure in the final rich-text rewrite must roll back the whole
        # section: no gallery, text unchanged, rows flagged failed.
        image = api.content.create(
            container=self.portal, type="Image", title="plone.png"
        )
        section = self._make_section(
            '<p>Avant <img src="resolveuid/%s" /> après</p>' % image.UID()
        )
        self.request.form["apply"] = "1"
        # RichTextValue is only used for the final write inside _migrate_images;
        # _make_section already ran with the real one above.
        with mock.patch(
            "imio.smartweb.core.browser.migration."
            "migrate_sectiontext_images.RichTextValue",
            side_effect=RuntimeError("boom"),
        ):
            view, html = self._render()

        galleries = [
            o
            for o in self.page.objectValues()
            if o.portal_type == "imio.smartweb.SectionGallery"
        ]
        self.assertEqual(len(galleries), 0)
        self.assertIn("<img", section.text.raw)
        entry = view.results[0]
        self.assertFalse(entry["gallery_created"])
        self.assertTrue(entry["error"])
        self.assertEqual(entry["images"][0]["status"], "failed")
        self.assertEqual(entry["images"][0]["reason"], "rollback de la section")

    def test_position_after_fallback_records_note(self):
        # If positioning raises, migration still succeeds and a note is kept.
        image = api.content.create(
            container=self.portal, type="Image", title="plone.png"
        )
        section = self._make_section('<p><img src="resolveuid/%s" /></p>' % image.UID())
        self.request.form["apply"] = "1"
        with mock.patch(
            "imio.smartweb.core.browser.migration."
            "migrate_sectiontext_images.IExplicitOrdering",
            side_effect=RuntimeError("no ordering"),
        ):
            view, html = self._render()

        galleries = [
            o
            for o in self.page.objectValues()
            if o.portal_type == "imio.smartweb.SectionGallery"
        ]
        self.assertEqual(len(galleries), 1)
        self.assertTrue(view.results[0]["position_note"])
        # migration itself still succeeded
        self.assertEqual(view.results[0]["images"][0]["status"], "migrated")
        self.assertNotIn("<img", section.text.raw)

    @requests_mock.Mocker()
    def test_download_external_image_ssl_error(self, m):
        import requests as rq

        url = "https://ex.org/badcert.png"
        m.get(url, exc=rq.exceptions.SSLError("bad cert"))
        _, _, _, error = _download_external_image(url, {})
        self.assertTrue(error.startswith("SSL error"))
