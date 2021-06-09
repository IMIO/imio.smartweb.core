# -*- coding: utf-8 -*-

from imio.smartweb.core.behaviors.minisite import IImioSmartwebMinisite
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from plone.app.layout.navigation.interfaces import INavigationRoot
from zope.component import getMultiAdapter
from zope.lifecycleevent import ObjectRemovedEvent
from zope.globalrequest import getRequest


def folder_moved(object, event):
    """We use IObjectMovedEvent instead of IObjectAddedEvent because Minisite interface is not yet
    provided when we use IObjectAddedEvent"""
    if not IImioSmartwebMinisite.providedBy(object):
        return
    if type(event) is ObjectRemovedEvent:
        # We don't have anything to do if minisite is being removed
        return
    if not INavigationRoot.providedBy(event.newParent):
        request = getRequest()
        minisite_settings = getMultiAdapter((object, request), name="minisite_settings")
        minisite_settings.disable()
        api.portal.show_message(
            _(
                u"Your Folder was a minisite but this behaviour has been disabled with this action"
            ),
            request,
            type="warning",
        )
