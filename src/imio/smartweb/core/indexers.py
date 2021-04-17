# -*- coding: utf-8 -*-

from imio.smartweb.core.contents import IPages
from imio.smartweb.core.contents import ISectionText
from plone import api
from plone.app.contenttypes.behaviors.leadimage import ILeadImage
from plone.app.contenttypes.indexers import SearchableText
from plone.app.contenttypes.indexers import _unicode_save_string_concat
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


@indexer(IPages)
def SearchableText_pages(obj):
    """Construct SearchableText of pages with SearchableText of its sections"""
    catalog = api.portal.get_tool("portal_catalog")
    result = _unicode_save_string_concat(SearchableText(obj))
    brains = api.content.find(context=obj, depth=1)
    for brain in brains:
        indexes = catalog.getIndexDataForRID(brain.getRID())
        searchable_text = indexes.get("SearchableText") or []
        result = " ".join((result, " ".join(searchable_text)))
    return result
