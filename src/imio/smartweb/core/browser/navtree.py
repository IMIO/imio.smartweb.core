# -*- coding: utf-8 -*-

from imio.smartweb.core.content import IDefaultPages
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from Products.CMFPlone.browser.navtree import (
    SitemapNavtreeStrategy as BaseSitemapNavtreeStrategy,
)
from zope.interface import implementer


@implementer(INavtreeStrategy)
class SitemapNavtreeStrategy(BaseSitemapNavtreeStrategy):
    """The navtree building strategy used by the sitemap, based on
    navtree_properties
    """

    def nodeFilter(self, node):
        """Remove default pages from site map"""
        provided = getattr(node["item"], "object_provides", [])
        return IDefaultPages.__identifier__ not in provided
