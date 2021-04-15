# -*- coding: utf-8 -*-

from plone.app.contenttypes.interfaces import IPloneAppContenttypesLayer
from zope.interface import Interface


class IImioSmartwebCoreLayer(IPloneAppContenttypesLayer):
    """Marker interface that defines a browser layer."""


class IImioSmartwebSubsiteMarker(Interface):
    """Marker interface for subsite."""
