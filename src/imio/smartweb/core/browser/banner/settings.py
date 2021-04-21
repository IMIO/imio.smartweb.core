# -*- coding: utf-8 -*-

from imio.smartweb.core.behaviors.subsite import IImioSmartwebSubsite
from imio.smartweb.core.contents import IFolder
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from plone.app.layout.navigation.interfaces import INavigationRoot
from Products.CMFPlone.interfaces.constrains import DISABLED
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from Products.CMFPlone.utils import safe_hasattr
from Products.Five.browser import BrowserView
from zope.interface import Interface
from zope.interface import alsoProvides
from zope.interface import noLongerProvides


class IHiddenLocalBanner(Interface):
    """"""


class BannerSettings(BrowserView):
    """Banner settings"""

    def switch_banner_display(self):
        if IHiddenLocalBanner.providedBy(self.context):
            noLongerProvides(self.context, IHiddenLocalBanner)
            message = _(u"Banner is now again displayed from this item")
        else:
            alsoProvides(self.context, IHiddenLocalBanner)
            message = _(u"Banner is now hidden from this item")
        api.portal.show_message(message, self.request)
        self.context.reindexObject(idxs=(["object_provides"]))
        self.request.response.redirect(self.context.absolute_url())
