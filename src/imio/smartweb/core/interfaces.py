# -*- coding: utf-8 -*-

from imio.smartweb.common.interfaces import IImioSmartwebCommonLayer
from plone.app.contenttypes.interfaces import IPloneAppContenttypesLayer


class IImioSmartwebCoreLayer(IImioSmartwebCommonLayer, IPloneAppContenttypesLayer):
    """Marker interface that defines a browser layer."""
