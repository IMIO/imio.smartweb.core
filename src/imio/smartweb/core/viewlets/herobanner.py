# -*- coding: utf-8 -*-

from Acquisition import aq_parent
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.layout.viewlets import common
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Products.CMFPlone.utils import base_hasattr


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
        if IPloneSiteRoot.providedBy(obj):
            pass
        else:
            if INavigationRoot.providedBy(obj):
                pass
            else:
                parent = aq_parent(obj)
                if not base_hasattr(parent, "default_page"):
                    is_a_default_page = False
                else:
                    is_a_default_page = (
                        parent.default_page == obj.id
                        and INavigationRoot.providedBy(parent)
                    )
                if not is_a_default_page:
                    return
                else:
                    obj = parent
        herobanners = obj.listFolderContents(
            contentFilter={"portal_type": "imio.smartweb.HeroBanner"}
        )
        if len(herobanners) > 0:
            self._herobanner = herobanners[0]
            return self._herobanner
