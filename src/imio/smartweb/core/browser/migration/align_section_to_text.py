# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.subscriber import (
    _enforce_text_alignment_width,
)
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five.browser import BrowserView
from zope.interface import alsoProvides

import logging

logger = logging.getLogger("imio.smartweb.core")

# Two migrations in one pass, on every imio.smartweb.Page and every
# imio.smartweb.Procedure (PortalPage, Footer, HeroBanner... are left alone):
#
#   - the page itself gets text_align_container = True
#   - each of its sections gets section_alignment = "text". SectionText is
#     excluded: it omits section_alignment and has its own "alignment" field.
#
#   /Plone/@@align_section_to_text            -> dry run, changes nothing
#   /Plone/@@align_section_to_text?apply=1    -> actually migrates

PAGE_TYPES = ("imio.smartweb.Page", "imio.smartweb.Procedure")
EXCLUDED_TYPES = ("imio.smartweb.SectionText",)


class AlignSectionToTextView(BrowserView):

    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        self.apply = self.request.form.get("apply") in ("1", "true", "True")
        self.pages_to_change = []
        self.pages_already_ok = []
        self.to_change = []
        self.already_ok = []
        self.stale = []

        section_types = self.section_types()
        for page_brain in api.content.find(portal_type=PAGE_TYPES):
            page_path = page_brain.getPath()
            try:
                page = page_brain.getObject()
            except (AttributeError, KeyError):
                # Stale catalog entry: the object behind it is gone. Its
                # sections are skipped too, they went away with it.
                self.stale.append(page_path)
                continue

            if page.text_align_container:
                self.pages_already_ok.append(page_path)
            else:
                self.pages_to_change.append(
                    {
                        "path": page_path,
                        "title": page_brain.Title,
                        "type": page_brain.portal_type,
                    }
                )
                if self.apply:
                    page.text_align_container = True
                    page.reindexObject()

            # Sections are direct children of the page, hence depth=1.
            for brain in api.content.find(
                path={"query": page_path, "depth": 1}, portal_type=section_types
            ):
                try:
                    obj = brain.getObject()
                except (AttributeError, KeyError):
                    self.stale.append(brain.getPath())
                    continue
                if obj.section_alignment == "text":
                    self.already_ok.append(brain.getPath())
                    continue
                self.to_change.append(
                    {
                        "path": brain.getPath(),
                        "title": brain.Title,
                        "type": brain.portal_type,
                        "page": page_path,
                        "old_alignment": obj.section_alignment,
                        "old_width": obj.bootstrap_css_class,
                    }
                )
                if self.apply:
                    obj.section_alignment = "text"
                    # Same rule as the section subscriber: a text aligned
                    # section only makes sense in full or half width.
                    _enforce_text_alignment_width(obj)
                    obj.reindexObject()

        if self.stale:
            logger.warning(
                "align_section_to_text: {} stale catalog entrie(s) skipped: "
                "{}".format(len(self.stale), ", ".join(self.stale))
            )
        if self.apply:
            logger.info(
                "align_section_to_text: {} page(s) switched to the text "
                "container, {} section(s) aligned on it".format(
                    len(self.pages_to_change), len(self.to_change)
                )
            )
        return self.index()

    def section_types(self):
        types_tool = api.portal.get_tool("portal_types")
        return [
            name
            for name in types_tool.objectIds()
            if name.startswith("imio.smartweb.Section") and name not in EXCLUDED_TYPES
        ]
