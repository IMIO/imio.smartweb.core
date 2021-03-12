# -*- coding: utf-8 -*-

from collective.behavior.gallery.interfaces import ICollectiveBehaviorGalleryLayer
from plone.app.contenttypes.interfaces import IPloneAppContenttypesLayer
from zope.interface import Interface


class IImioSmartwebCoreLayer(
    IPloneAppContenttypesLayer, ICollectiveBehaviorGalleryLayer
):
    """Marker interface that defines a browser layer."""


class IImioSmartwebSubsite(Interface):
    """Marker interface for subsite."""
