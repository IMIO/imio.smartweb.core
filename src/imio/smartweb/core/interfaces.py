# -*- coding: utf-8 -*-
from collective.anysurfer.interfaces import ILayerSpecific
from imio.smartweb.common.interfaces import IImioSmartwebCommonLayer
from plone.app.contenttypes.interfaces import IPloneAppContenttypesLayer


class IImioSmartwebCoreLayer(
    IImioSmartwebCommonLayer, IPloneAppContenttypesLayer, ILayerSpecific
):
    """Marker interface that defines a browser layer."""
