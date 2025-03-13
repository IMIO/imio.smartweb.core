# -*- coding: utf-8 -*-

from collective.anysurfer.interfaces import ILayerSpecific
from collective.messagesviewlet.interfaces import ICollectiveMessagesviewletLayer
from collective.solr.browser.interfaces import IThemeSpecific
from imio.smartweb.common.interfaces import IImioSmartwebCommonLayer
from plone.app.contenttypes.interfaces import IPloneAppContenttypesLayer
from Products.CMFPlone.browser.interfaces import ISiteMap
from zope.interface import Interface


class ISmartwebIcon(Interface):
    """Marker interface to easily find all registered icons in registry."""


class IViewWithoutLeadImage(Interface):
    """Marker interface for views that shouldn't show leadimage."""


class IImioSmartwebCoreLayer(
    IImioSmartwebCommonLayer,
    IPloneAppContenttypesLayer,
    ILayerSpecific,
    IThemeSpecific,
    ICollectiveMessagesviewletLayer,
    ISiteMap,
):
    """Marker interface that defines a browser layer."""


class IImioIdeaboxLayer(Interface):
    """Marker interface that defines a browser layer."""


class IArcgisViewUtils(Interface):
    """ """

    def get_portal_item_id():
        """Return id of a map"""


class IOgpViewUtils(Interface):
    """ """


class IOdwbViewUtils(Interface):
    """ """

    def is_odwb_widget_plugins():
        """Return True if we are in the generic odwb widget plugins"""


class IHtmxViewUtils(Interface):
    """ """
