# -*- coding: utf-8 -*-
from imio.smartweb.core.behaviors.minisite import IImioSmartwebMinisite
from plone import api
from plone.app.layout.viewlets.common import LogoViewlet as baseLogoViewlet
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class LogoViewlet(baseLogoViewlet):
    """ """

    index_minisite = ViewPageTemplateFile("logo.pt")

    def render(self):
        root = api.portal.get_navigation_root(self.context)
        if IImioSmartwebMinisite.providedBy(root):
            return self.index_minisite()
        else:
            return self.index()

    def show_logo(self):
        root = api.portal.get_navigation_root(self.context)
        if root.logo is None:
            return False
        return root.logo_display_mode in ["logo", "logo_title"]

    def show_title(self):
        root = api.portal.get_navigation_root(self.context)
        return root.logo_display_mode in ["title", "logo_title"]
