# -*- coding: utf-8 -*-

from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.layout.viewlets import common


class HeroBannerViewlet(common.ViewletBase):

    _herobanner = None

    def available(self):
        return self.herobanner is not None

    def update(self):
        if not self.available():
            return
        # we don't want to show edition tools in herobanner sections
        self.request.set("can_edit", False)
        self.sections = self.herobanner.listFolderContents()

    @property
    def herobanner(self):
        if self._herobanner is not None:
            return self._herobanner
        if not INavigationRoot.providedBy(self.context):
            return
        herobanners = self.context.listFolderContents(
            contentFilter={"portal_type": "imio.smartweb.HeroBanner"}
        )
        if len(herobanners) > 0:
            self._herobanner = herobanners[0]
            return self._herobanner
