# -*- coding: utf-8 -*-

from imio.smartweb.common.caching import ban_physicalpath
from imio.smartweb.core.contents import IPages
from imio.smartweb.core.contents import Pages
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.autoform.directives import write_permission
from plone.supermodel import model
from Products.CMFPlone.utils import parent
from zope import schema
from zope.globalrequest import getRequest
from zope.interface import implementer


class IHeroBanner(IPages):
    """Marker interface and Dexterity Python Schema for hero banner"""

    model.fieldset("layout", label=_("Layout"), fields=["css_class"])

    write_permission(css_class="cmf.ManagePortal")
    css_class = schema.TextLine(title=_("CSS class"), default="", required=False)


@implementer(IHeroBanner)
class HeroBanner(Pages):
    """Hero banner class"""

    def notifyModified(self):
        super(HeroBanner, self).notifyModified()
        request = getRequest()
        physical_path = parent(self).getPhysicalPath()
        ban_physicalpath(request, physical_path)
