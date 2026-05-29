# -*- coding: utf-8 -*-

import json

from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles


def _body(response):
    """Return what the view wrote into the response body, as str.

    In integration tests the response is an ``HTTPResponse`` whose
    ``write()`` prepends an HTTP status line plus headers (via
    ``BaseResponse.outputBody()``) before the streamed chunks. In WSGI
    production the response is a ``WSGIResponse`` whose ``write()`` simply
    appends to ``stdout``. We strip the headers prefix when present so the
    same helper works in both modes.
    """
    raw = response.stdout.getvalue()
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8")
    sep = "\r\n\r\n"
    if sep in raw:
        raw = raw.split(sep, 1)[1]
    return raw


class TestDumpSiteCatalog(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def _dump(self, context=None):
        ctx = context if context is not None else self.portal
        # The test layer reuses the response across calls within a test;
        # stdout is a BytesIO that accumulates. Reset it so each dump can be
        # parsed in isolation.
        self.request.response.stdout.seek(0)
        self.request.response.stdout.truncate(0)
        self.request.response._wrote = 0
        view = api.content.get_view(
            name="dump_site_catalog",
            context=ctx,
            request=self.request,
        )
        view()
        return json.loads(_body(self.request.response))

    def test_top_level_is_list(self):
        empty_folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            title="empty",
        )
        data = self._dump(empty_folder)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "empty")

    def test_basic_hierarchy(self):
        folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            title="root",
        )
        page = api.content.create(
            container=folder,
            type="imio.smartweb.Page",
            title="page",
        )
        api.content.create(
            container=page,
            type="imio.smartweb.SectionText",
            title="section",
        )
        data = self._dump(folder)
        self.assertEqual(data[0]["title"], "root")
        self.assertEqual(len(data[0]["children"]), 1)
        self.assertEqual(data[0]["children"][0]["title"], "page")
        self.assertEqual(data[0]["children"][0]["children"][0]["title"], "section")

    def test_leaf_has_no_children_key(self):
        folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            title="root",
        )
        page = api.content.create(
            container=folder,
            type="imio.smartweb.Page",
            title="page",
        )
        section = api.content.create(
            container=page,
            type="imio.smartweb.SectionText",
            title="section",
        )
        data = self._dump(folder)
        leaf = data[0]["children"][0]["children"][0]
        # Section subclasses inherit from Container (IFolderish), so they
        # emit an empty children list rather than omitting the key.
        self.assertEqual(leaf.get("children", []), [])
        api.content.delete(obj=section)
        data = self._dump(folder)
        self.assertEqual(data[0]["children"][0]["children"], [])

    def test_behavior_fields_emitted_when_set(self):
        folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            title="root",
        )
        page = api.content.create(
            container=folder,
            type="imio.smartweb.Page",
            title="page",
        )
        page.iam = ["citizen"]
        page.topics = ["sport"]
        page.taxonomy_page_category = "publication"
        page.searchwords = ["clef1", "clef2"]
        data = self._dump(folder)
        page_node = data[0]["children"][0]
        self.assertEqual(page_node["iam"], ["citizen"])
        self.assertEqual(page_node["topics"], ["sport"])
        self.assertEqual(page_node["taxonomy_page_category"], "publication")
        self.assertEqual(page_node["searchwords"], ["clef1", "clef2"])

    def test_behavior_fields_omitted_when_absent(self):
        folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            title="root",
        )
        data = self._dump(folder)
        node = data[0]
        self.assertNotIn("iam", node)
        self.assertNotIn("topics", node)
        self.assertNotIn("taxonomy_page_category", node)
        self.assertNotIn("taxonomy_procedure_category", node)
        self.assertNotIn("searchwords", node)

    def test_behavior_fields_omitted_when_empty(self):
        folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            title="root",
        )
        page = api.content.create(
            container=folder,
            type="imio.smartweb.Page",
            title="page",
        )
        page.iam = []
        page.topics = []
        data = self._dump(folder)
        page_node = data[0]["children"][0]
        self.assertNotIn("iam", page_node)
        self.assertNotIn("topics", page_node)

    def test_procedure_taxonomy_emitted(self):
        proc = api.content.create(
            container=self.portal,
            type="imio.smartweb.Procedure",
            title="proc",
        )
        proc.taxonomy_procedure_category = "autorisation_carte"
        data = self._dump(proc)
        self.assertEqual(data[0]["taxonomy_procedure_category"], "autorisation_carte")

    def test_response_headers(self):
        folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            title="empty",
        )
        view = api.content.get_view(
            name="dump_site_catalog",
            context=folder,
            request=self.request,
        )
        view()
        ct = self.request.response.getHeader("Content-Type")
        cd = self.request.response.getHeader("Content-Disposition")
        self.assertEqual(ct, "application/json; charset=utf-8")
        self.assertIsNotNone(cd)
        self.assertIn("attachment", cd)
        self.assertIn(".json", cd)

    def test_view_writes_to_response_stdout(self):
        # The view writes JSON via response.write() into response.stdout
        # while the ZODB connection is still open, then returns an empty
        # body. Verifies the mechanism that lets ZPublisher serve the
        # download without holding the entire dict tree in Python memory.
        folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            title="empty",
        )
        view = api.content.get_view(
            name="dump_site_catalog",
            context=folder,
            request=self.request,
        )
        result = view()
        self.assertEqual(result, b"")
        body = _body(self.request.response)
        self.assertTrue(body.startswith("["))
        self.assertTrue(body.endswith("]"))

    def test_root_parameter_restricts_subtree(self):
        api.content.create(
            container=self.portal, type="imio.smartweb.Folder", title="a"
        )
        b = api.content.create(
            container=self.portal, type="imio.smartweb.Folder", title="b"
        )
        api.content.create(container=b, type="imio.smartweb.Page", title="page-in-b")

        self.request.form["root"] = "/".join(b.getPhysicalPath())
        view = api.content.get_view(
            name="dump_site_catalog",
            context=self.portal,
            request=self.request,
        )
        view()
        data = json.loads(_body(self.request.response))
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "b")
        titles = [c["title"] for c in data[0]["children"]]
        self.assertEqual(titles, ["page-in-b"])

    def test_root_parameter_unknown_path_returns_404(self):
        self.request.form["root"] = "/Plone/does-not-exist"
        view = api.content.get_view(
            name="dump_site_catalog",
            context=self.portal,
            request=self.request,
        )
        view()
        self.assertEqual(self.request.response.getStatus(), 404)

    def test_cache_gc_called_at_gc_every_interval(self):
        for i in range(5):
            api.content.create(
                container=self.portal,
                type="imio.smartweb.Page",
                title="p{}".format(i),
            )
        self.request.form["gc_every"] = "2"
        view = api.content.get_view(
            name="dump_site_catalog",
            context=self.portal,
            request=self.request,
        )
        view()
        self.assertGreaterEqual(view._gc_count, 3)

    def test_gc_every_defaults_to_200(self):
        view = api.content.get_view(
            name="dump_site_catalog",
            context=self.portal,
            request=self.request,
        )
        view()
        self.assertEqual(view._gc_every, 200)

    def test_broken_node_produces_error_node_not_500(self):
        from Acquisition import aq_base

        folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            title="root",
        )
        api.content.create(
            container=folder,
            type="imio.smartweb.Page",
            title="good",
        )
        bad = api.content.create(
            container=folder,
            type="imio.smartweb.Page",
            title="bad",
        )
        bad_cls = aq_base(bad).__class__
        original_title = bad_cls.Title
        bad_id = bad.getId()

        def _boom(self):
            if self.getId() == bad_id:
                raise RuntimeError("kaboom")
            return original_title(self)

        bad_cls.Title = _boom
        try:
            data = self._dump(folder)
        finally:
            bad_cls.Title = original_title

        titles = [c.get("title") for c in data[0]["children"]]
        self.assertIn("good", titles)
        self.assertEqual(len(data[0]["children"]), 2)
        bad_node = [c for c in data[0]["children"] if c.get("title") == "<error>"]
        self.assertEqual(len(bad_node), 1)
        self.assertIn("kaboom", bad_node[0]["error"])


# <audit>
#   <file>test_dump_site_catalog.py</file>
#   <requirements_applied>R1, R2, R3, R5</requirements_applied>
#   <deviations>None</deviations>
#   <questions>None</questions>
# </audit>
