# -*- coding: utf-8 -*-

from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.dexterity.content import Item
from zope import schema
from zope.interface import implementer
from zope.interface import Interface


class IPublication(Interface):
    """ """

    # title = schema.TextLine(title=_("Title"), required=True)

    # description = schema.Text(title=_("Description"), required=False)

    linked_publication = schema.Choice(
        vocabulary="imio.smartweb.vocabulary.IADeliberationsPublications",
        title=_("I.A. Deliberation publication"),
        required=True,
        default=None,
    )


@implementer(IPublication)
class Publication(Item):
    """Publication class"""
