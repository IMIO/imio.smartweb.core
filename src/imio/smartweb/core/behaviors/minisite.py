# -*- coding: utf-8 -*-

from imio.smartweb.core.contents import IFolder
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.autoform.interfaces import IFormFieldProvider
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


class IImioSmartwebMinisite(INavigationRoot):
    """Marker interface to use minisite as a new navigation root"""


@provider(IFormFieldProvider)
class IImioSmartwebMinisiteSettings(model.Schema):

    model.fieldset(
        "layout",
        label=_(u"Layout"),
        fields=["logo", "logo_display_mode"],
    )

    logo = NamedBlobImage(
        title=_(u"Logo"),
        description=_(u"Define a logo for minisite"),
        required=False,
    )

    logo_display_mode = schema.Choice(
        title=_(u"Logo display"),
        description=_(u"Choose your display mode"),
        source="imio.smartweb.vocabulary.SubsiteDisplayMode",
        required=True,
        default="title",
    )


@implementer(IImioSmartwebMinisiteSettings)
@adapter(IFolder)
class Minisite(object):
    """ """
