# -*- coding: utf-8 -*-

from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.dexterity.content import Container
from plone.namedfile.field import NamedBlobImage
from zope.interface import implementer
from zope import schema
from zope.schema import TextLine
from zope.schema.interfaces import ITextLine
from plone.app.contenttypes.interfaces import ILink


class ILinkField(ITextLine):
    """ """


@implementer(ILinkField)
class LinkField(TextLine):
    """ """


class IBlockLink(ILink):
    """Marker interface and Dexterity Python Schema for BlockLink"""

    title = schema.TextLine(title=_("Title"), required=True)

    description = schema.Text(title=_("Description"), required=False)

    open_in_new_tab = schema.Bool(
        title=_("Open in a new tab"), required=False, default=False
    )

    remoteUrl = LinkField(title=_("URL"), required=True)

    image = NamedBlobImage(title=_("Image"), required=False)

    svg_icon = schema.Choice(
        title=_("Icon"),
        description=_("Only used in table view (takes precedence over image)"),
        source="imio.smartweb.vocabulary.Icons",
        required=False,
    )


@implementer(IBlockLink)
class BlockLink(Container):
    """BlockLink class"""
