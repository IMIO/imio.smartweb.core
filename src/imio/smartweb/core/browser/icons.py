# -*- coding: utf-8 -*-

from io import BytesIO
from lxml import etree
from Products.CMFPlone.browser.icons import IconsView
from Products.CMFPlone.browser.icons import SVG_MODIFER
from zExceptions import NotFound
from zope.component.hooks import getSite
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

import logging

logger = logging.getLogger("imio.smartweb.core")


@implementer(IPublishTraverse)
class SmartwebIconsView(IconsView):
    prefix = "smartweb.icon."

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

    def tag(self, name, tag_class="", tag_alt=""):
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
