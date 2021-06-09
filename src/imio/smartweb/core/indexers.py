# -*- coding: utf-8 -*-

from imio.smartweb.core.contents import IFolder
from imio.smartweb.core.contents import IPages
from imio.smartweb.core.contents import ISection
from imio.smartweb.core.contents import ISectionText
from plone import api
from plone.app.contenttypes.behaviors.leadimage import ILeadImage
from plone.app.contenttypes.indexers import SearchableText
from plone.app.contenttypes.indexers import _unicode_save_string_concat
from plone.dexterity.interfaces import IDexterityContent
from plone.indexer.decorator import indexer
from plone.app.contenttypes.behaviors.richtext import IRichText


@indexer(IDexterityContent)
def has_leadimage(obj):
    if ILeadImage.providedBy(obj) and getattr(obj, "image", False):
        return True
    return False


@indexer(ISection)
def SearchableText_section(obj):
    if obj.hide_title:
        # Don't index titles that are hidden to the visitor
        return ""
    return obj.title or ""


@indexer(ISectionText)
def SearchableText_sectiontext(obj):
    """Title is always hidden in text sections, so we only index text field"""
    transforms = api.portal.get_tool("portal_transforms")
    textvalue = IRichText(obj).text
    raw = textvalue.raw
    text = (
        transforms.convertTo("text/plain", raw, mimetype=textvalue.mimeType)
        .getData()
        .strip()
    )
    return text


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


@indexer(IFolder)
def related_quickaccess(obj):
    if obj.quick_access_items is None:
        return []
    return [item.to_object.UID() for item in obj.quick_access_items]
