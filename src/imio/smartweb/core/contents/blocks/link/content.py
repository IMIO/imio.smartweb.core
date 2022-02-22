# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.blocks.link.fields import IconsRadioWidget
from imio.smartweb.core.contents.blocks.link.fields import LinkField
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.app.contenttypes.interfaces import ILink
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class IBlockLink(ILink):
    """Marker interface and Dexterity Python Schema for BlockLink"""

    title = schema.TextLine(title=_("Title"), required=True)

    description = schema.Text(title=_("Description"), required=False)

    open_in_new_tab = schema.Bool(
        title=_("Open in a new tab"), required=False, default=False
    )

    remoteUrl = LinkField(title=_("URL"), required=True)

    image = NamedBlobImage(title=_("Image"), required=False)

    model.fieldset("icons", label=_("Icons"), fields=["svg_icon"])
    directives.widget("svg_icon", IconsRadioWidget)
    svg_icon = schema.Choice(
        title=_("Link illustration icon"),
        description=_("Only used in table view (takes precedence over image)"),
        source="imio.smartweb.vocabulary.Icons",
        required=False,
    )


@implementer(IBlockLink)
class BlockLink(Container):
    """BlockLink class"""
