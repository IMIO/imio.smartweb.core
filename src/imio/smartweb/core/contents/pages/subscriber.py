# -*- coding: utf-8 -*-
from imio.smartweb.core.contents import IDefaultPages
from zope.interface import noLongerProvides


def remove_default_page(obj, event):
    """Remove "pages" (i.s.Procedure, i.s.Page) marked as a default page out of a imio.smartweb.Folder"""
    noLongerProvides(obj, IDefaultPages)
    folder = obj.aq_parent
    folder.default_page_uid = None
