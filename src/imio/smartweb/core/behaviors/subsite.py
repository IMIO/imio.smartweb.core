# -*- coding: utf-8 -*-

from imio.smartweb.core.contents import IFolder
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.autoform.interfaces import IFormFieldProvider
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IImioSmartwebSubsite(model.Schema):

    model.fieldset(
        "layout",
        label=_(u"Layout"),
        fields=["banner", "logo", "logo_display_mode", "menu_depth"],
    )

    banner = NamedBlobImage(
        title=_(u"Banner"),
        description=_(u"Define a banner for subsite and children"),
        required=False,
    )

    logo = NamedBlobImage(
        title=_(u"Logo"),
        description=_(u"Define a logo for subsite and children"),
        required=False,
    )

    logo_display_mode = schema.Choice(
        title=_(u"Logo display"),
        description=_(u"Choose your display mode"),
        source="imio.smartweb.vocabulary.SubsiteDisplayMode",
        required=True,
        default="title",
    )

    menu_depth = schema.Int(
        title=_(u"Menu depth"),
        description=_(u"Define number of levels in menu navigation subsite"),
        required=True,
        default=1,
    )


@implementer(IImioSmartwebSubsite)
@adapter(IFolder)
class Subsite(object):
    """"""
