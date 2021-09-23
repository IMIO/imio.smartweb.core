# -*- coding: utf-8 -*-

from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class IDirectoryView(model.Schema):
    """Marker interface and Dexterity Python Schema for DirectoryView"""

    nb_results = schema.Int(
        title=_(u"Number of items to display"), default=20, required=True
    )

    see_more_link = schema.URI(title=_(u"See more link"), required=False)

    selected_entity = schema.Choice(
        title=_(u"Selected entity"),
        description=_(u"Select entity to display"),
        vocabulary="imio.smartweb.vocabulary.RemoteDirectoryEntities",
        required=True,
    )

    show_items_description = schema.Bool(
        title=_(u"Show items description"), default=True, required=False
    )


@implementer(IDirectoryView)
class DirectoryView(Container):
    """DirectoryView class"""
