# -*- coding: utf-8 -*-

from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.dexterity.content import Container
from plone.namedfile.field import NamedBlobImage
from zope.interface import implementer
from zope.schema import Bool
from zope.schema import Text
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

    title = TextLine(title=_(u"Title"), required=True)
    description = Text(title=_(u"Description"), required=False)
    open_in_new_tab = Bool(title=_(u"Open in a new tab"), required=False, default=False)
    remoteUrl = LinkField(title=_(u"URL"), required=True)
    image = NamedBlobImage(title=_(u"Image"), required=False)


@implementer(IBlockLink)
class BlockLink(Container):
    """BlockLink class"""
