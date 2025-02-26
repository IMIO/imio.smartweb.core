# -*- coding: utf-8 -*-

from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from plone.app.layout.viewlets import common
from zope.component import getMultiAdapter
from zope.i18n import translate
from zope.viewlet.interfaces import IViewletManager


class HeaderActionsViewlet(common.ViewletBase):
    def update(self):
        context_state = getMultiAdapter(
            (self.context, self.request), name="plone_context_state"
        )
        language = api.portal.get_current_language(context=self.context)
        self.actions = context_state.actions("header_actions")
        for action in self.actions:
            if action["id"] == "account":
                action["link_target"] = "_blank"
                desc = translate(_(action["description"]), target_language=language)
                new_tab = translate(_("New tab"), target_language=language)
                action["description"] = f"{desc} ({new_tab})"


class HeaderActionsContainerViewlet(common.ViewletBase):
    """Viewlet containing the header actions viewlets manager"""


class IHeaderActionsViewletsManager(IViewletManager):
    """Viewlet manager containing header actions viewlets"""
