# -*- coding: utf-8 -*-

from Acquisition import aq_parent
from imio.smartweb.core.utils import reindexParent


def _enforce_text_alignment_width(obj):
    if obj.section_alignment == "text" and obj.bootstrap_css_class not in (
        None,
        "",
        "col-sm-12",
        "col-sm-6",
    ):
        # Only full width or half width make sense when aligned with the
        # text sections container.
        obj.bootstrap_css_class = "col-sm-12"


def added_section(obj, event):
    if obj.collapsible_section:
        obj.hide_title = False
    _enforce_text_alignment_width(obj)
    reindexParent(obj, event)


def modified_section(obj, event):
    if obj.collapsible_section:
        obj.hide_title = False
    _enforce_text_alignment_width(obj)
    reindexParent(obj, event)


def removed_section(obj, event):
    if event.newParent is None:
        return
    parent = aq_parent(obj)
    if parent is not None:
        # in some cases (ex: relation breaking), we do not get the object in
        # its acquisition chain
        parent.reindexObject()
