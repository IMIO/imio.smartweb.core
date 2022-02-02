# -*- coding: utf-8 -*-

from Acquisition import aq_parent
from imio.smartweb.core.contents.sections.base import ISection


def modified_section_content(obj, event):
    parent = aq_parent(obj)
    if parent is None:
        return
    if ISection.providedBy(parent):
        page = aq_parent(parent)
        page.reindexObject()
