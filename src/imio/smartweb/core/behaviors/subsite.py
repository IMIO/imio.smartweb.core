# -*- coding: utf-8 -*-

from imio.smartweb.core.contents import IFolder
from imio.smartweb.core.contents.cropping import SmartwebCroppingProvider
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.autoform.interfaces import IFormFieldProvider
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


class SubsiteCroppingProvider(SmartwebCroppingProvider):
    def get_scales(self, fieldname, request=None):
        if fieldname == "logo":
            # scale used for logo field
            return ["preview"]
        else:
            return super(SubsiteCroppingProvider, self).get_scales(fieldname, request)


@provider(IFormFieldProvider)
class IImioSmartwebSubsite(model.Schema):
    model.fieldset(
        "layout",
        label=_("Layout"),
        fields=["logo", "logo_display_mode"],
    )

    logo = NamedBlobImage(
        title=_("Logo"),
        description=_("Define a logo for subsite and children"),
        required=False,
    )

    logo_display_mode = schema.Choice(
        title=_("Logo display"),
        description=_("Choose your display mode"),
        source="imio.smartweb.vocabulary.SubsiteDisplayMode",
        required=True,
        default="title",
    )

    model.fieldset("settings", fields=["menu_depth"])
    menu_depth = schema.Int(
        title=_("Menu depth"),
        description=_("Define number of levels in menu navigation subsite"),
        required=True,
        default=2,
    )


@implementer(IImioSmartwebSubsite)
@adapter(IFolder)
class Subsite(object):
    """ """
