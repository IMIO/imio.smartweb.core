# -*- coding: utf-8 -*-

from imio.smartweb.common.interfaces import ILocalManagerAware
from imio.smartweb.core.contents import IFolder
from imio.smartweb.core.contents.cropping import SmartwebCroppingProvider
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.autoform.directives import write_permission
from plone.autoform.interfaces import IFormFieldProvider
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


class MinisiteCroppingProvider(SmartwebCroppingProvider):
    def get_scales(self, fieldname, request=None):
        if fieldname == "logo":
            # scale used for logo field
            return ["preview"]
        else:
            return super(MinisiteCroppingProvider, self).get_scales(fieldname, request)


class IImioSmartwebMinisite(INavigationRoot, ILocalManagerAware):
    """Marker interface to use minisite as a new navigation root"""


@provider(IFormFieldProvider)
class IImioSmartwebMinisiteSettings(model.Schema):
    model.fieldset(
        "layout",
        label=_("Layout"),
        fields=["logo", "logo_display_mode"],
    )

    write_permission(logo="imio.smartweb.core.CanEditMinisiteLogo")
    logo = NamedBlobImage(
        title=_("Logo"),
        description=_("Define a logo for minisite"),
        required=False,
    )

    logo_display_mode = schema.Choice(
        title=_("Logo display"),
        description=_("Choose your display mode"),
        source="imio.smartweb.vocabulary.SubsiteDisplayMode",
        required=True,
        default="title",
    )


@implementer(IImioSmartwebMinisiteSettings)
@adapter(IFolder)
class Minisite(object):
    """ """
