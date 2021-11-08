# -*- coding: utf-8 -*-

from collective.anysurfer.interfaces import ILayerSpecific
from collective.solr.browser.interfaces import IThemeSpecific
from imio.smartweb.common.interfaces import IImioSmartwebCommonLayer
from plone.app.contenttypes.interfaces import IPloneAppContenttypesLayer
from zope.interface import Interface


class IViewWithoutLeadImage(Interface):
    """Marker interface for views that shouldn't show leadimage."""


class IImioSmartwebCoreLayer(
    IImioSmartwebCommonLayer, IPloneAppContenttypesLayer, ILayerSpecific, IThemeSpecific
):
    """Marker interface that defines a browser layer."""
