# -*- coding: utf-8 -*-

from imio.smartweb.core.contents import IPages
from imio.smartweb.core.contents import Pages
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.autoform.directives import write_permission
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class IHeroBanner(IPages):
    """Marker interface and Dexterity Python Schema for hero banner"""

    model.fieldset("layout", label=_("Layout"), fields=["css_class"])

    write_permission(css_class="cmf.ManagePortal")
    css_class = schema.TextLine(title=_("CSS class"), default="", required=False)


@implementer(IHeroBanner)
class HeroBanner(Pages):
    """Hero banner class"""
