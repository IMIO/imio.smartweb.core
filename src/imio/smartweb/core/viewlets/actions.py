# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import common
from zope.component import getMultiAdapter
from zope.viewlet.interfaces import IViewletManager


class HeaderActionsViewlet(common.ViewletBase):
    def update(self):
        context_state = getMultiAdapter(
            (self.context, self.request), name="plone_context_state"
        )
        self.actions = context_state.actions("header_actions")


class HeaderActionsContainerViewlet(common.ViewletBase):
    """Viewlet containing the header actions viewlets manager"""


class IHeaderActionsViewletsManager(IViewletManager):
    """Viewlet manager containing header actions viewlets"""
