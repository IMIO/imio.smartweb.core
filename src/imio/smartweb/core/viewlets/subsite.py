# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from Acquisition import aq_parent
from imio.smartweb.core.behaviors.subsite import IImioSmartwebSubsite
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.layout.viewlets import common
from plone.app.layout.viewlets.common import GlobalSectionsViewlet
from plone.memoize.view import memoize
from Products.CMFPlone.browser.navigation import CatalogNavigationTabs
from zope.component import getMultiAdapter


class SubsiteNavigationTabs(CatalogNavigationTabs):
    navtree_path = None

    def _getNavQuery(self):
        query = super(SubsiteNavigationTabs, self)._getNavQuery()
        query["path"]["query"] = self.navtree_path
        return query


class BaseSubsiteViewlet(common.ViewletBase):
    _subsite_root = None

    @property
    def subsite_root(self):
        if self._subsite_root is not None:
            return self._subsite_root
        obj = self.context
        while not IImioSmartwebSubsite.providedBy(
            obj
        ) and not INavigationRoot.providedBy(obj):
            obj = aq_parent(aq_inner(obj))
        if IImioSmartwebSubsite.providedBy(obj):
            self._subsite_root = obj
            return self._subsite_root

    def available(self):
        return self.subsite_root is not None


class SubsiteNavigationViewlet(BaseSubsiteViewlet, GlobalSectionsViewlet):
    @property
    def navtree_path(self):
        return "/".join(self.subsite_root.getPhysicalPath())

    @property
    def navtree_depth(self):
        return self.subsite_root.menu_depth

    @property
    @memoize
    def portal_tabs(self):
        subsite_tabs_view = getMultiAdapter(
            (self.context, self.request), name="subsite_tabs_view"
        )
        subsite_tabs_view.navtree_path = self.navtree_path
        return subsite_tabs_view.topLevelTabs(actions=[])


class SubsiteLogoViewlet(BaseSubsiteViewlet):
    def show_logo(self):
        if self.subsite_root.logo is None:
            return False
        return self.subsite_root.logo_display_mode in ["logo", "logo_title"]

    def show_title(self):
        return self.subsite_root.logo_display_mode in ["title", "logo_title"]
