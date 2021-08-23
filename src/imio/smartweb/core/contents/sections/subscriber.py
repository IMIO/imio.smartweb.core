# -*- coding: utf-8 -*-

from Acquisition import aq_parent


def reindexParent(obj, event):
    parent = aq_parent(obj)
    if parent is not None:
        # in some cases (ex: relation breaking), we do not get the object in
        # its acquisition chain
        parent.reindexObject()
