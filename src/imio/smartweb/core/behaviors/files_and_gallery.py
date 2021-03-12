# -*- coding: utf-8 -*-

from collective.behavior.gallery.behaviors.folderish_gallery import IFolderishGallery
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.interface import provider
from zope.schema.interfaces import IContextSourceBinder


@provider(IContextSourceBinder)
def contained_images(context):
    query = {
        "portal_type": "Image",
        "path": {"query": "/".join(context.getPhysicalPath()), "depth": 1},
    }
    return CatalogSource(context, **query)


@provider(IContextSourceBinder)
def contained_files(context):
    query = {
        "portal_type": "File",
        "path": {"query": "/".join(context.getPhysicalPath()), "depth": 1},
    }
    return CatalogSource(context, **query)


@provider(IFormFieldProvider)
class IFilteredFilesAndGallery(IFolderishGallery):
    """"""
    directives.widget(
        "selected_images",
        RelatedItemsFieldWidget,
        pattern_options={
            "mode": "auto",
            "favorites": [],
        },
    )
    selected_images = RelationList(
        title=_(u"Selected images"),
        value_type=RelationChoice(
            source=contained_images,
        ),
        required=False,
    )

    directives.widget(
        "selected_files",
        RelatedItemsFieldWidget,
        pattern_options={
            "mode": "auto",
            "favorites": [],
        },
    )
    selected_files = RelationList(
        title=_(u"Selected files"),
        value_type=RelationChoice(
            source=contained_files,
        ),
        required=False,
    )
