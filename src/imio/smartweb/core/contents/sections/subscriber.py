# -*- coding: utf-8 -*-

from Acquisition import aq_parent


def added_section(obj, event):
    if obj.collapsible_section:
        obj.hide_title = False
    reindexParent(obj, event)


def modified_section(obj, event):
    if obj.collapsible_section:
        obj.hide_title = False
    reindexParent(obj, event)


def reindexParent(obj, event):
    parent = aq_parent(obj)
    if parent is not None:
        # in some cases (ex: relation breaking), we do not get the object in
        # its acquisition chain
        parent.reindexObject()
