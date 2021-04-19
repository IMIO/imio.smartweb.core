# -*- coding: utf-8 -*-

from plone.app.contenttypes.interfaces import IPloneAppContenttypesLayer
from plone.app.z3cform.interfaces import IPloneFormLayer
from plone.theme.interfaces import IDefaultPloneLayer


class IImioSmartwebCoreLayer(
    IDefaultPloneLayer, IPloneAppContenttypesLayer, IPloneFormLayer
):
    """Marker interface that defines a browser layer."""
