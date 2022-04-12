# -*- coding: utf-8 -*-

from Acquisition import aq_parent
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.layout.viewlets import common
from Products.CMFPlone.defaultpage import get_default_page


class HeroBannerViewlet(common.ViewletBase):

    _herobanner = None

    def available(self):
        return self.herobanner is not None

    def update(self):
        if not self.available():
            return
        # we need to tell the template that we are rendering for the viewlet
        self.request.set("viewlet_rendering", True)
        # we don't want to show edition tools in herobanner sections
        self.request.set("can_edit", False)
        self.sections = self.herobanner.listFolderContents()

    @property
    def herobanner(self):
        if self._herobanner is not None:
            return self._herobanner

        obj = self.context
        if not INavigationRoot.providedBy(obj):
            parent = aq_parent(obj)
            if not INavigationRoot.providedBy(parent):
                return

            default_page = get_default_page(parent)
            if default_page == obj.id:
                obj = parent
            else:
                return

        herobanners = obj.listFolderContents(
            contentFilter={"portal_type": "imio.smartweb.HeroBanner"}
        )
        if len(herobanners) > 0:
            self._herobanner = herobanners[0]
            return self._herobanner
