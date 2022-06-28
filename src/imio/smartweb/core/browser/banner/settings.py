# -*- coding: utf-8 -*-

from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from Products.Five.browser import BrowserView
from zope.interface import Interface
from zope.interface import alsoProvides
from zope.interface import noLongerProvides


class ILocallyHiddenBanner(Interface):
    """ """


class BannerSettings(BrowserView):
    """Banner settings"""

    def switch_banner_display(self):
        if ILocallyHiddenBanner.providedBy(self.context):
            noLongerProvides(self.context, ILocallyHiddenBanner)
            message = _("Banner is now again displayed from this item")
        else:
            alsoProvides(self.context, ILocallyHiddenBanner)
            message = _("Banner is now hidden from this item")
        api.portal.show_message(message, self.request)
        self.context.reindexObject(idxs=["object_provides"])
        self.request.response.redirect(self.context.absolute_url())
