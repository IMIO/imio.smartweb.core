# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from plone.app.contenttypes.interfaces import IPloneAppContenttypesLayer
from zope.interface import Interface


class IImioSmartwebCoreLayer(IPloneAppContenttypesLayer):
    """Marker interface that defines a browser layer."""


class IImioSmartwebSubsite(Interface):
    """Marker interface for subsite."""
