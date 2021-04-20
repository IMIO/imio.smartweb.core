# -*- coding: utf-8 -*-

from plone.dexterity.content import Container
from zope.interface import Interface
from zope.interface import implementer


class IPages(Interface):
    """Shared base marker interface and schema for Pages"""


class IDefaultPages(Interface):
    """
    Marker interfaces for default Pages in Element view
    """


@implementer(IPages)
class Pages(Container):
    """Shared base class for Pages"""

    def canSetDefaultPage(self):
        return False
