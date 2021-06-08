# -*- coding: utf-8 -*-

from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from collective.instancebehavior import disable_behaviors
from collective.instancebehavior import enable_behaviors
from imio.smartweb.core.behaviors.minisite import IImioSmartwebMinisite
from imio.smartweb.core.behaviors.minisite import IImioSmartwebMinisiteSettings
from imio.smartweb.core.behaviors.subsite import IImioSmartwebSubsite
from imio.smartweb.core.contents import IFolder
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from Products.Five.browser import BrowserView
from zope.interface import alsoProvides
from zope.interface import noLongerProvides


class MiniSiteSettings(BrowserView):
    """Subsite settings"""

    def enable(self):
        enable_behaviors(
            self.context,
            [IImioSmartwebMinisiteSettings.__identifier__],
            [IImioSmartwebMinisiteSettings],
        )
        alsoProvides(self.context, IImioSmartwebMinisite)
        self.context.exclude_from_nav = True
        self.context.reindexObject(idxs=("object_provides", "exclude_from_nav"))
        api.portal.show_message(
            _(u"Minisite has been successfully activated"), self.request
        )
        self.request.response.redirect(self.context.absolute_url())

    def disable(self):
        disable_behaviors(
            self.context,
            [IImioSmartwebMinisiteSettings.__identifier__],
            [IImioSmartwebMinisiteSettings],
        )
        noLongerProvides(self.context, IImioSmartwebMinisite)
        self.context.exclude_from_nav = False
        self.context.reindexObject(idxs=("object_provides", "exclude_from_nav"))
        api.portal.show_message(_(u"Minisite has been disabled"), self.request)
        self.request.response.redirect(self.context.absolute_url())

    @property
    def available(self):
        if IPloneSiteRoot.providedBy(self.context):
            # PloneSite can't become minisite
            return False
        if not IPloneSiteRoot.providedBy(self.context.aq_parent):
            # Minisite can only be added in PloneSite
            return False
        if IImioSmartwebSubsite.providedBy(self.context):
            # Subsite can't be converted in minisite
            return False
        return IFolder.providedBy(self.context) and not self.enabled

    @property
    def enabled(self):
        return IImioSmartwebMinisite.providedBy(self.context)
