# -*- coding: utf-8 -*-

from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five.browser import BrowserView
from zope.interface import alsoProvides

import logging

logger = logging.getLogger("imio.smartweb.core")

# On every imio.smartweb.Page and every imio.smartweb.Procedure (PortalPage,
# Footer, HeroBanner... are left alone), set text_align_container = False.
# Nothing else is touched: sections keep their section_alignment and width.
#
#   /Plone/@@text_align_container_false            -> dry run, changes nothing
#   /Plone/@@text_align_container_false?apply=1    -> actually migrates

PAGE_TYPES = ("imio.smartweb.Page", "imio.smartweb.Procedure")


class TextAlignContainerFalseView(BrowserView):

    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        self.apply = self.request.form.get("apply") in ("1", "true", "True")
        self.pages_to_change = []
        self.pages_already_ok = []
        self.stale = []

        for page_brain in api.content.find(portal_type=PAGE_TYPES):
            page_path = page_brain.getPath()
            try:
                page = page_brain.getObject()
            except (AttributeError, KeyError):
                # Stale catalog entry: the object behind it is gone.
                self.stale.append(page_path)
                continue

            if not page.text_align_container:
                self.pages_already_ok.append(page_path)
                continue
            self.pages_to_change.append(
                {
                    "path": page_path,
                    "title": page_brain.Title,
                    "type": page_brain.portal_type,
                }
            )
            if self.apply:
                page.text_align_container = False
                page.reindexObject()

        if self.stale:
            logger.warning(
                "text_align_container_false: {} stale catalog entrie(s) skipped: "
                "{}".format(len(self.stale), ", ".join(self.stale))
            )
        if self.apply:
            logger.info(
                "text_align_container_false: {} page(s) switched off the text "
                "container".format(len(self.pages_to_change))
            )
        return self.index()
