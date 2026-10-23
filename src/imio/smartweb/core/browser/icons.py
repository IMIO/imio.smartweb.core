# -*- coding: utf-8 -*-

from io import BytesIO
from lxml import etree
from Products.CMFPlone.browser.icons import IconsView
from Products.CMFPlone.browser.icons import SVG_MODIFER
from plone.registry.interfaces import IRegistry
from zExceptions import NotFound
from zope.component import getUtility
from zope.component.hooks import getSite
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

import logging

logger = logging.getLogger("imio.smartweb.core")


@implementer(IPublishTraverse)
class SmartwebIconsView(IconsView):
    prefix = "smartweb.icon."

    def _datagrid_icon(self, name):
        if not name:
            return None
        rows = getUtility(IRegistry).get("smartweb.svg_icon_preview_rows", []) or []
        for row in rows:
            if row.get("icon_name") == name and row.get("svg_file"):
                return row.get("svg_file")
        return None

    def __call__(self):
        svg_file = self._datagrid_icon(getattr(self, "name", None))
        if svg_file:
            self.request.response.setHeader("Content-Type", "image/svg+xml")
            return svg_file.encode("utf-8")
        return super().__call__()

    def _iconfile(self, icon):
        site = getSite()
        try:
            # Use unrestrictedTraverse to handle icons stored in portal_resources
            return site.unrestrictedTraverse(icon)
        except NotFound:
            logger.exception(
                f"Icon resolver lookup of '{icon}' failed, fallback to Plone icon."
            )
            return site.restrictedTraverse(self.defaulticon)

    def _svg_tag(self, svg_file, tag_class="", tag_alt=""):
        fh = BytesIO(svg_file.encode("utf-8"))
        try:
            svgtree = etree.parse(fh)
        except etree.XMLSyntaxError:
            logger.exception("SVG File from smartweb.svg_icon_preview_rows")
            return svg_file
        if svgtree.docinfo.root_name.lower() != "svg":
            raise ValueError(
                "SVG file content root tag mismatch "
                f"(not svg but {svgtree.docinfo.root_name})"
            )
        self._ensure_viewbox(svgtree)
        modifier_cfg = {
            "cssclass": tag_class,
            "title": tag_alt,
        }
        for name, modifier in SVG_MODIFER.items():
            __traceback_info__ = name
            modifier(svgtree, modifier_cfg)
        return etree.tostring(svgtree)

    def _ensure_viewbox(self, svgtree):
        # Uploaded SVG files may only define width / height : without viewBox,
        # they are cropped instead of being scaled when resized with CSS
        root = svgtree.getroot()
        if root.get("viewBox"):
            return
        try:
            width = float(root.get("width", "").replace("px", ""))
            height = float(root.get("height", "").replace("px", ""))
        except ValueError:
            return
        root.set("viewBox", f"0 0 {width:g} {height:g}")

    def tag(self, name, tag_class="", tag_alt=""):
        svg_file = self._datagrid_icon(name)
        if svg_file:
            return self._svg_tag(svg_file, tag_class, tag_alt)
        try:
            return super(SmartwebIconsView, self).tag(name, tag_class, tag_alt)
        except NotImplementedError:
            # Resolving icon stored in database, let's do it below
            # See https://github.com/plone/Products.CMFPlone/pull/3359
            pass
        icon = self.lookup(name)
        iconfile = self._iconfile(icon)
        fh = BytesIO(iconfile.data)
        try:
            svgtree = etree.parse(fh)
        except etree.XMLSyntaxError:
            logger.exception(f"SVG File from Database: {iconfile.absolute_url()}")
            return iconfile.data

        if svgtree.docinfo.root_name.lower() != "svg":
            raise ValueError(
                f"SVG file content root tag mismatch (not svg but {svgtree.docinfo.root_name}): {iconfile.path}"
            )
        modifier_cfg = {
            "cssclass": tag_class,
            "title": tag_alt,
        }
        for name, modifier in SVG_MODIFER.items():
            __traceback_info__ = name
            modifier(svgtree, modifier_cfg)
        return etree.tostring(svgtree)
