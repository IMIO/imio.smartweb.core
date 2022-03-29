# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import common
from zope.viewlet.interfaces import IViewletManager


class PortalHeaderTopContainerViewlet(common.ViewletBase):
    """Viewlet containing the top header viewlets manager"""


class IPortalHeaderTopContainerViewletManager(IViewletManager):
    """Viewlet manager containing top header viewlets"""
