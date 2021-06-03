# -*- coding: utf-8 -*-

from imio.smartweb.core.browser.minisite.settings import IImioSmartwebMinisite
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from plone.app.layout.navigation.interfaces import INavigationRoot
from zope.globalrequest import getRequest
from zope.interface import noLongerProvides


def folder_moved(object, event):
    """We use IObjectMovedEvent instead of IObjectAddedEvent because Minisite interface is not yet
    provided when we use IObjectAddedEvent"""
    if not IImioSmartwebMinisite.providedBy(object):
        return
    if not INavigationRoot.providedBy(event.newParent):
        noLongerProvides(object, IImioSmartwebMinisite)
        request = getRequest()
        api.portal.show_message(
            _(
                u"Your Folder was a minisite but this behaviour has been disabled with this action"
            ),
            request,
            type="warning",
        )
