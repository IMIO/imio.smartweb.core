# -*- coding: utf-8 -*-
from plone.app.contenttypes.behaviors.leadimage import ILeadImage
from plone.dexterity.interfaces import IDexterityContent
from plone.indexer.decorator import indexer


@indexer(IDexterityContent)
def has_leadimage(obj):
    if ILeadImage.providedBy(obj) and getattr(obj, "image", False):
        return True
    return False
