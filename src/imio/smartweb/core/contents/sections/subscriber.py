# -*- coding: utf-8 -*-

from imio.smartweb.core.utils import reindexParent


def added_section(obj, event):
    if obj.collapsible_section:
        obj.hide_title = False
    reindexParent(obj, event)


def modified_section(obj, event):
    if obj.collapsible_section:
        obj.hide_title = False
    reindexParent(obj, event)
