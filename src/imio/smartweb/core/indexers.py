# -*- coding: utf-8 -*-

from imio.smartweb.core.contents import ISectionText
from plone.app.contenttypes.behaviors.leadimage import ILeadImage
from plone.app.contenttypes.indexers import _unicode_save_string_concat
from plone.app.contenttypes.indexers import SearchableText
from plone.dexterity.interfaces import IDexterityContent
from plone.indexer.decorator import indexer


@indexer(IDexterityContent)
def has_leadimage(obj):
    if ILeadImage.providedBy(obj) and getattr(obj, "image", False):
        return True
    return False


@indexer(ISectionText)
def SearchableText_sectiontext(obj):
    return _unicode_save_string_concat(SearchableText(obj))
