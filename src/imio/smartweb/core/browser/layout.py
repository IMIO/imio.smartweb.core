# -*- coding: utf-8 -*-
from collective.anysurfer.layout import LayoutPolicy as AnysurferLayoutPolicy
from eea.facetednavigation.config import ANNO_FACETED_LAYOUT
from eea.facetednavigation.subtypes.interfaces import IFacetedNavigable
from imio.smartweb.core.behaviors.minisite import IImioSmartwebMinisite
from imio.smartweb.core.viewlets.banner import BannerViewlet
from imio.smartweb.core.viewlets.subsite import BaseSubsiteViewlet
from plone import api
from plone.app.layout.globals import layout as base
from zope.annotation.interfaces import IAnnotations


class LayoutPolicy(AnysurferLayoutPolicy):
    """
    Enhanced layout policy
    """

    def bodyClass(self, template, view):
        """
        Extend Plone to add a CSS class on <body> based on :
         1. banner image
         2. minisite
         3. subsite
         4. faceted layout
        """
        context = self.context
        request = self.request

        # Get default body classes
        body_class = base.LayoutPolicy.bodyClass(self, template, view)

        # 1. Add bloc-banner class if there is a banner on the page
        banner_viewlet = BannerViewlet(context, request, view)
        if banner_viewlet.available() and not banner_viewlet.is_banner_locally_hidden:
            body_class += " bloc-banner"

        # 2. Add is-in-minisite class to body if we are in a minisite
        root = api.portal.get_navigation_root(context)
        if IImioSmartwebMinisite.providedBy(root):
            body_class += " is-in-minisite"

        # 3. Add is-in-subsite class to body if we are in a subsite
        subsite_viewlet = BaseSubsiteViewlet(context, request, view)
        if subsite_viewlet.available():
            body_class += " is-in-subsite"

        # 4. Add faceted class to body if a faceted layout is define
        if IFacetedNavigable.providedBy(context):
            faceted_layout = IAnnotations(self.context).get(
                ANNO_FACETED_LAYOUT, "faceted-block-view"
            )
            body_class += f" {faceted_layout}"
        return body_class
