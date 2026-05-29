# -*- coding: utf-8 -*-

import json
import logging
import transaction

from datetime import date
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from plone.uuid.interfaces import IUUID
from Products.CMFCore.interfaces import IContentish
from Products.CMFCore.interfaces import IFolderish
from Products.Five.browser import BrowserView
from zope.interface import alsoProvides

logger = logging.getLogger("imio.smartweb.core.dump_site_catalog")


def _json(value):
    """Compact, UTF-8-safe JSON encoding of a single value."""
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


_OPTIONAL_FIELDS = (
    "iam",
    "topics",
    "taxonomy_page_category",
    "taxonomy_procedure_category",
    "searchwords",
)


class DumpSiteCatalogView(BrowserView):
    """Stream the site tree as a hierarchical JSON list."""

    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        self._count = 0
        self._gc_count = 0
        try:
            self._gc_every = max(1, int(self.request.form.get("gc_every", 200)))
        except (TypeError, ValueError):
            self._gc_every = 200
        portal = api.portal.get()
        root_path = self.request.form.get("root")
        if root_path:
            try:
                root = portal.unrestrictedTraverse(str(root_path))
            except (KeyError, AttributeError):
                self.request.response.setStatus(404)
                self.request.response.setHeader(
                    "Content-Type", "text/plain; charset=utf-8"
                )
                return "root path not found: {}".format(root_path)
        else:
            root = self.context
        response = self.request.response
        response.setHeader("Content-Type", "application/json; charset=utf-8")
        portal_id = api.portal.get().getId()
        filename = "site_catalog_{}_{}.json".format(portal_id, date.today().isoformat())
        response.setHeader(
            "Content-Disposition",
            'attachment; filename="{}"'.format(filename),
        )
        # ZPublisher closes the ZODB connection before the WSGI body is
        # iterated, so we cannot return the generator directly. We drain the
        # generator into response.stdout via response.write() while the
        # connection is still open. The Python heap stays small because we
        # never build the full dict tree, and the ZODB cache is bounded by
        # _maybe_gc().
        for chunk in self._iter_chunks(root):
            if isinstance(chunk, str):
                chunk = chunk.encode("utf-8")
            response.write(chunk)
        return b""

    def _iter_chunks(self, root):
        yield "["
        for chunk in self._iter_node(root, first=True):
            yield chunk
        yield "]"

    def _iter_node(self, obj, first):
        # Resolve every field that might raise before yielding the first byte.
        # On failure, the whole node is replaced by an error node — the JSON
        # stream stays valid because nothing was emitted yet. Children are
        # isolated by their own recursive _iter_node call.
        try:
            fields = self._extract_fields(obj)
            is_container = IFolderish.providedBy(obj)
        except Exception as exc:
            logger.exception("dump_site_catalog: failed to extract node fields")
            if not first:
                yield ","
            yield "{"
            yield '"uid":' + _json("?")
            yield ',"title":' + _json("<error>")
            yield ',"error":' + _json("{}: {}".format(type(exc).__name__, exc))
            yield "}"
            return
        if not first:
            yield ","
        yield "{"
        yield '"uid":' + _json(fields["uid"])
        yield ',"title":' + _json(fields["title"])
        yield ',"path":' + _json(fields["path"])
        yield ',"portal_type":' + _json(fields["portal_type"])
        yield ',"review_state":' + _json(fields["review_state"])
        for name in _OPTIONAL_FIELDS:
            value = fields.get(name)
            if value:
                yield "," + _json(name) + ":" + _json(value)
        if is_container:
            yield ',"children":['
            try:
                children = list(obj.objectValues())
            except Exception:
                logger.exception("dump_site_catalog: failed to list children")
                children = []
            child_first = True
            for child in children:
                if not IContentish.providedBy(child):
                    continue
                for chunk in self._iter_node(child, first=child_first):
                    yield chunk
                child_first = False
            yield "]"
        yield "}"
        self._maybe_gc(obj)
        if not is_container:
            try:
                obj._p_deactivate()
            except Exception:
                pass

    def _extract_fields(self, obj):
        return {
            "uid": IUUID(obj, None),
            "title": obj.Title() or "",
            "path": "/".join(obj.getPhysicalPath()),
            "portal_type": getattr(obj, "portal_type", None),
            "review_state": api.content.get_state(obj=obj, default=None),
            "iam": getattr(obj, "iam", None),
            "topics": getattr(obj, "topics", None),
            "taxonomy_page_category": getattr(obj, "taxonomy_page_category", None),
            "taxonomy_procedure_category": getattr(
                obj, "taxonomy_procedure_category", None
            ),
            "searchwords": getattr(obj, "searchwords", None),
        }

    def _maybe_gc(self, obj):
        self._count += 1
        if self._count % self._gc_every == 0:
            transaction.savepoint(optimistic=True)
            jar = getattr(obj, "_p_jar", None)
            if jar is not None:
                jar.cacheGC()
            self._gc_count += 1
