# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import common
from zope.component import getMultiAdapter


class HeaderActionsViewlet(common.ViewletBase):
    def update(self):
        context_state = getMultiAdapter(
            (self.context, self.request), name=u"plone_context_state"
        )
        self.actions = context_state.actions("header_actions")
