# -*- coding: utf-8 -*-

from imio.smartweb.core.contents import IPages
from imio.smartweb.core.contents import Pages
from zope.interface import implementer


class IPortalPage(IPages):
    """Marker interface and Dexterity Python Schema for PortalPage"""


@implementer(IPortalPage)
class PortalPage(Pages):
    """PortalPage class"""
