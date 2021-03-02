# -*- coding: utf-8 -*-

from imio.smartweb.core.contents import IFolder
from imio.smartweb.core.interfaces import IImioSmartwebSubsite
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from Products.Five.browser import BrowserView
from zope.interface import alsoProvides
from zope.interface import noLongerProvides


class SubSiteSettings(BrowserView):
    """Subsite settings"""

    @property
    def enable(self):
        alsoProvides(self.context, IImioSmartwebSubsite)
        self.context.reindexObject(idxs=('object_provides'))
        api.portal.show_message(_(u"Subsite has been successfully activated"), self.request)
        self.request.response.redirect(self.context.absolute_url())

    @property
    def disable(self):
        noLongerProvides(self.context, IImioSmartwebSubsite)
        self.context.reindexObject(idxs=('object_provides'))
        api.portal.show_message(_(u"Subsite has been disabled"), self.request)
        self.request.response.redirect(self.context.absolute_url())

    @property
    def available(self):
        return IFolder.providedBy(self.context) and not self.enabled

    @property
    def enabled(self):
        return IImioSmartwebSubsite.providedBy(self.context)
