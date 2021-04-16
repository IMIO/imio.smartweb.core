# -*- coding: utf-8 -*-

from imio.smartweb.core.behaviors.subsite import IImioSmartwebSubsite
from plone import api
from Acquisition import aq_base
from Acquisition import aq_inner
from Acquisition import aq_parent
from plone.app.layout.viewlets import common
from zope.component import getMultiAdapter


class BaseSubsiteViewlet(common.ViewletBase):
    _subsite_root = None

    @property
    def subsite_root(self):
        if self._subsite_root is not None:
            return self._subsite_root
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
            self._subsite_root = obj
            return self._subsite_root

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
