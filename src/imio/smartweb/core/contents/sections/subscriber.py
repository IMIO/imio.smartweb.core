# -*- coding: utf-8 -*-

from Acquisition import aq_parent


def reindexParent(obj, event):
    parent = aq_parent(obj)
    parent.reindexObject()
