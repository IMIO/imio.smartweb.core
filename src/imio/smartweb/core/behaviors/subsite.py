# -*- coding: utf-8 -*-

from imio.smartweb.core.interfaces import IImioSmartwebSubsite
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.autoform.interfaces import IFormFieldProvider
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider
from plone.dexterity.interfaces import IDexterityContent


@provider(IFormFieldProvider)
class ISubsite(model.Schema):

    menu_depth = schema.Int(
        title=_(u"Menu depth"),
        description=_(u"Define number of levels in menu navigation subsite"),
        required=True,
        default=1,
    )

    logo = NamedBlobImage(
        title=_(u"Logo"),
        description=_(u"Define a logo for subsite"),
        required=False,
    )

    logo_display = schema.Choice(
        title=_(u"Logo display"),
        description=_(u"Choose your display mode"),
        source="imio.smartweb.vocabulary.SubsiteDisplayMode",
        required=True,
        default="title",
    )


@implementer(ISubsite)
@adapter(IImioSmartwebSubsite)
class Subsite(object):
    """"""

    def __init__(self, context):
        self.context = context
