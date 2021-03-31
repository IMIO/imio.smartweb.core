# -*- coding: utf-8 -*-

from imio.smartweb.core.interfaces import IImioSmartwebSubsite
from plone import api
from Acquisition import aq_base
from Acquisition import aq_inner
from Acquisition import aq_parent
from plone.app.layout.viewlets import common
from zope.component import getMultiAdapter


class SubsiteNavigationViewlet(common.ViewletBase):

    @property
    def subsite_root(self):
        obj = self.context
        portal = api.portal.get()
        while not IImioSmartwebSubsite.providedBy(obj) and aq_base(obj) is not aq_base(
            portal
        ):
            parent = aq_parent(aq_inner(obj))
            if parent is None:
                return None
            obj = parent
        if IImioSmartwebSubsite.providedBy(obj):
            return obj

    def available(self):
        return self.subsite_root is not None

    def get_items(self):
        view = getMultiAdapter((self.subsite_root, self.request), name="block_view")
        return view.blocks_results()
