# -*- coding: utf-8 -*-

from imio.smartweb.core.contents import IFolder
from imio.smartweb.core.contents import IPage
from imio.smartweb.core.contents import IPages
from imio.smartweb.core.contents import ISection
from imio.smartweb.core.contents import ISectionText
from imio.smartweb.core.utils import concat_voca_term
from plone import api
from plone.app.contenttypes.behaviors.richtext import IRichText
from plone.app.contenttypes.indexers import SearchableText
from plone.app.contenttypes.indexers import _unicode_save_string_concat
from plone.dexterity.interfaces import IDexterityContent
from plone.indexer.decorator import indexer
from Products.CMFPlone.utils import base_hasattr


@indexer(IDexterityContent)
def exclude_from_parent_listing(obj):
    if base_hasattr(obj, "exclude_from_parent_listing"):
        return obj.exclude_from_parent_listing
    return False


@indexer(ISection)
def SearchableText_section(obj):
    terms = []
    if not obj.hide_title:
        # Only index titles that are shown to the visitor
        terms.append(obj.title)
    if base_hasattr(obj, "description") and obj.description:
        # Index descriptinons (if any) withould bold
        terms.append(obj.description.replace("**", ""))
    return " ".join(terms)


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


@indexer(IPage)
def concat_category_topics_indexer(obj):
    category = getattr(obj.aq_base, "page_category", None)
    topics = getattr(obj.aq_base, "topics", [])

    index = []
    if not category and not topics:
        return index
    if topics:
        for topic in topics:
            index.append(concat_voca_term(category, topic))
    else:
        index = category
    return index
