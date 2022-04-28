# -*- coding: utf-8 -*-

from Acquisition import aq_parent
from imio.smartweb.core.utils import get_default_content_id
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.layout.viewlets import common


class HeroBannerViewlet(common.ViewletBase):

    _herobanner = None

    def available(self):
        return self.herobanner is not None

    def update(self):
        if not self.available():
            return
        # we need to tell the template that we are rendering for the viewlet
        self.request.set("viewlet_rendering", True)
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

            default_page_id = get_default_content_id(parent)
            if default_page_id == obj.id:
                obj = parent
            else:
                return

        herobanners = obj.listFolderContents(
            contentFilter={"portal_type": "imio.smartweb.HeroBanner"}
        )
        if len(herobanners) > 0:
            self._herobanner = herobanners[0]
            return self._herobanner
