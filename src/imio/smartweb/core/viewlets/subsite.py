# -*- coding: utf-8 -*-

from Acquisition import aq_base
from Acquisition import aq_inner
from Acquisition import aq_parent
from imio.smartweb.core.interfaces import IImioSmartwebSubsiteMarker
from plone import api
from plone.app.layout.viewlets import common
from zope.component import getMultiAdapter


class BaseSubsiteViewlet(common.ViewletBase):
    @property
    def subsite_root(self):
        obj = self.context
        portal = api.portal.get()
        while not IImioSmartwebSubsiteMarker.providedBy(obj) and aq_base(
            obj
        ) is not aq_base(portal):
            parent = aq_parent(aq_inner(obj))
            if parent is None:
                return None
            obj = parent
        if IImioSmartwebSubsiteMarker.providedBy(obj):
            return obj

    def available(self):
        return self.subsite_root is not None


class SubsiteNavigationViewlet(BaseSubsiteViewlet):
    def get_items(self):
        view = getMultiAdapter((self.subsite_root, self.request), name="block_view")
        return view.blocks_results()


class SubsiteLogoViewlet(BaseSubsiteViewlet):
    def show_logo(self):
        if self.subsite_root.logo is None:
            return False
        return self.subsite_root.logo_display_mode in ["logo", "logo_title"]

    def show_title(self):
        return self.subsite_root.logo_display_mode in ["title", "logo_title"]
