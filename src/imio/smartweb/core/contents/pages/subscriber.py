# -*- coding: utf-8 -*-
from imio.smartweb.core.contents import IDefaultPages
from zope.interface import noLongerProvides


def remove_default_page(obj, event):
    """
    Handle removal (cut/paste or delete) of a default page (i.s.Procedure, i.s.Page)
    from a folder
    """
    noLongerProvides(obj, IDefaultPages)
    obj.exclude_from_nav = False
    obj.reindexObject()
    folder = obj.aq_parent
    folder.default_page_uid = None
