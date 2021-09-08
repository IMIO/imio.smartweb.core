# -*- coding: utf-8 -*-

from imio.smartweb.core.behaviors.subsite import IImioSmartwebSubsite
from imio.smartweb.core.viewlets.navigation import ImprovedGlobalSectionsViewlet
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.layout.viewlets import common
from plone.memoize.view import memoize
from Products.CMFPlone.browser.navigation import CatalogNavigationTabs
from Products.CMFPlone.utils import parent
from zope.component import getMultiAdapter
from zope.viewlet.interfaces import IViewletManager


class SubsiteNavigationTabs(CatalogNavigationTabs):
    navtree_path = None

    def _getNavQuery(self):
        query = super(SubsiteNavigationTabs, self)._getNavQuery()
        query["path"]["query"] = self.navtree_path
        return query


class SubsiteHeaderViewlet(common.ViewletBase):
    """Viewlet containing the subsite header viewlets manager"""


class SubsiteHeaderViewletsManager(IViewletManager):
    """Viewlet manager containing subsite header viewlets"""


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
            obj = parent(obj)
        if IImioSmartwebSubsite.providedBy(obj):
            self._subsite_root = obj
            return self._subsite_root

    def available(self):
        return self.subsite_root is not None


class SubsiteNavigationViewlet(BaseSubsiteViewlet, ImprovedGlobalSectionsViewlet):
    @property
    def navtree_path(self):
        return "/".join(self.subsite_root.getPhysicalPath())

    @property
    def navtree_depth(self):
        return self.subsite_root.menu_depth

    @property
    def nav_root(self):
        return self.subsite_root

    @property
    @memoize
    def root_depth(self):
        return len(self.subsite_root.getPhysicalPath())

    @property
    @memoize
    def portal_tabs(self):
        subsite_tabs_view = getMultiAdapter(
            (self.context, self.request), name="subsite_tabs_view"
        )
        subsite_tabs_view.navtree_path = self.navtree_path
        return subsite_tabs_view.topLevelTabs(actions=[])

    def render_globalnav(self):
        self.remove_subsites_children()
        return self.build_tree(self.navtree_path)


class SubsiteLogoViewlet(BaseSubsiteViewlet):
    def show_logo(self):
        if self.subsite_root.logo is None:
            return False
        return self.subsite_root.logo_display_mode in ["logo", "logo_title"]

    def show_title(self):
        return self.subsite_root.logo_display_mode in ["title", "logo_title"]
