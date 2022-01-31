# -*- coding: utf-8 -*-

from imio.smartweb.common.faceted.utils import configure_faceted
from imio.smartweb.core.behaviors.minisite import IImioSmartwebMinisite
from imio.smartweb.core.utils import safe_html
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from plone.app.layout.navigation.interfaces import INavigationRoot
from zope.component import getMultiAdapter
from zope.lifecycleevent import ObjectRemovedEvent
from zope.globalrequest import getRequest

import os


def moved_folder(obj, event):
    """We use IObjectMovedEvent instead of IObjectAddedEvent because Minisite interface is not yet
    provided when we use IObjectAddedEvent"""
    if not IImioSmartwebMinisite.providedBy(obj):
        return
    if type(event) is ObjectRemovedEvent:
        # We don't have anything to do if minisite is being removed
        return
    if not INavigationRoot.providedBy(event.newParent):
        request = getRequest()
        minisite_settings = getMultiAdapter((obj, request), name="minisite_settings")
        minisite_settings.disable()
        api.portal.show_message(
            _(
                "Your Folder was a minisite but this behaviour has been disabled with this action"
            ),
            request,
            type="warning",
        )


def added_collection(obj, event):
    faceted_config_path = "{}/faceted/config/collection.xml".format(
        os.path.dirname(__file__)
    )
    configure_faceted(obj, faceted_config_path)


def added_sectionhtml(obj, event):
    obj.html = safe_html(obj.html)


def modified_sectionhtml(obj, event):
    obj.html = safe_html(obj.html)
