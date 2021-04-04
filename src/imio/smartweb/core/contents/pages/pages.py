# -*- coding: utf-8 -*-

from plone.dexterity.content import Container
from Products.CMFPlone.interfaces import IHideFromBreadcrumbs
from zope.interface import Interface
from zope.interface import implementer


class IPages(Interface):
    """Shared base marker interface and schema for Pages"""


class IDefaultPages(IHideFromBreadcrumbs):
    """
    Marker interfaces for default Pages in Element view
    Inheritance from IHideFromBreadcrumbs allows to automatically remove (hide)
    default pages from breadcrumbs.
    """


@implementer(IPages)
class Pages(Container):
    """Shared base class for Pages"""

    def canSetDefaultPage(self):
        return False
