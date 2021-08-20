# -*- coding: utf-8 -*-

from imio.smartweb.core.viewlets.banner import BannerViewlet
from plone.app.layout.globals import layout as base


class LayoutPolicy(base.LayoutPolicy):
    """
    Enhanced layout policy
    """

    def bodyClass(self, template, view):
        """
        Extend Plone to add a CSS class on <body> based on :
         1. banner image
        """
        context = self.context
        request = self.request

        # Get default body classes
        body_class = base.LayoutPolicy.bodyClass(self, template, view)

        # Add bloc-banner class if there is a banner on the page
        banner_viewlet = BannerViewlet(context, request, view)
        if banner_viewlet.available() and not banner_viewlet.is_banner_locally_hidden:
            body_class += " bloc-banner"
        return body_class
