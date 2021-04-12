# -*- coding: utf-8 -*-

from imio.smartweb.core.contents import IDefaultPages
from zope.interface import noLongerProvides


def paste_default_page(obj, event):
    """Handle cut/copy & paste / rename of a default page (Procedure / Page)"""
    if event.oldParent == event.newParent and event.oldName != event.newName:
        # page was simply renamed
        return
    noLongerProvides(obj, IDefaultPages)
    obj.exclude_from_nav = False
    obj.reindexObject(idxs=("object_provides", "exclude_from_nav"))
    parent = event.oldParent
    if parent is not None:
        # page was cut from a folder
        parent.default_page_uid = None


def remove_default_page(obj, event):
    """Handle removal of a default page (Procedure / Page) from a folder"""
    noLongerProvides(obj, IDefaultPages)
    obj.exclude_from_nav = False
    obj.reindexObject(idxs=("object_provides", "exclude_from_nav"))
    folder = obj.aq_parent
    folder.default_page_uid = None
