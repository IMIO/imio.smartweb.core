# -*- coding: utf-8 -*-

from imio.smartweb.core.contents import IPages
from imio.smartweb.core.contents import Pages
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.autoform.directives import write_permission
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class IFooter(IPages):
    """Marker interface and Dexterity Python Schema for Footer"""

    model.fieldset(
        "layout", label=_(u"Layout"), fields=["background_image", "css_class"]
    )

    write_permission(background_image="cmf.ManagePortal")
    background_image = NamedBlobImage(
        title=_(u"Set a background image"),
        required=False,
    )

    write_permission(css_class="cmf.ManagePortal")
    css_class = schema.TextLine(title=_(u"CSS class"), required=False)


@implementer(IFooter)
class Footer(Pages):
    """Footer class"""
