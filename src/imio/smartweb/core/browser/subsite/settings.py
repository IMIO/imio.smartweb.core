# -*- coding: utf-8 -*-

from collective.instancebehavior import disable_behaviors
from collective.instancebehavior import enable_behaviors
from imio.smartweb.core.behaviors.subsite import IImioSmartwebSubsite
from imio.smartweb.core.behaviors.minisite import IImioSmartwebMinisite
from imio.smartweb.core.contents import IFolder
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from Products.Five.browser import BrowserView


class SubSiteSettings(BrowserView):
    """Subsite settings"""

    def enable(self):
        enable_behaviors(
            self.context,
            [IImioSmartwebSubsite.__identifier__],
            [IImioSmartwebSubsite],
        )
        api.portal.show_message(
            _(u"Subsite has been successfully activated"), self.request
        )
        self.request.response.redirect(self.context.absolute_url())

    def disable(self):
        disable_behaviors(
            self.context,
            [IImioSmartwebSubsite.__identifier__],
            [IImioSmartwebSubsite],
        )
        api.portal.show_message(_(u"Subsite has been disabled"), self.request)
        self.request.response.redirect(self.context.absolute_url())

    @property
    def available(self):
        if IImioSmartwebMinisite.providedBy(self.context):
            return False
        return IFolder.providedBy(self.context) and not self.enabled

    @property
    def enabled(self):
        if IImioSmartwebMinisite.providedBy(self.context):
            return False
        return IImioSmartwebSubsite.providedBy(self.context)
