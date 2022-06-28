# -*- coding: utf-8 -*-

from imio.smartweb.common.caching import ban_physicalpath
from imio.smartweb.core.contents import IPages
from imio.smartweb.core.contents import Pages
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.autoform.directives import write_permission
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from Products.CMFPlone.utils import parent
from zope import schema
from zope.globalrequest import getRequest
from zope.interface import implementer


class IFooter(IPages):
    """Marker interface and Dexterity Python Schema for Footer"""

    model.fieldset(
        "layout", label=_("Layout"), fields=["background_image", "css_class"]
    )

    write_permission(background_image="cmf.ManagePortal")
    background_image = NamedBlobImage(
        title=_("Background image"),
        required=False,
    )

    write_permission(css_class="cmf.ManagePortal")
    css_class = schema.TextLine(title=_("CSS class"), default="", required=False)


@implementer(IFooter)
class Footer(Pages):
    """Footer class"""

    def notifyModified(self):
        super(Footer, self).notifyModified()
        request = getRequest()
        container = parent(self)
        if not container:
            return
        physical_path = container.getPhysicalPath()
        ban_physicalpath(request, physical_path)
