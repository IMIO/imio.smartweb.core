# -*- coding: utf-8 -*-

from imio.smartweb.core.utils import get_scale_url
from imio.smartweb.core.behaviors.minisite import IImioSmartwebMinisite
from plone import api
from plone.app.layout.viewlets.common import LogoViewlet as baseLogoViewlet
from plone.formwidget.namedfile.converter import b64decode_file
from plone.namedfile.utils import get_contenttype
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.interfaces import ISiteSchema
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility


def is_svg(filename):
    content_type = get_contenttype(filename=filename)
    return content_type == "image/svg+xml"


class LogoViewlet(baseLogoViewlet):
    """ """

    index = ViewPageTemplateFile("logo.pt")

    show_logo = True
    show_title = False
    is_svg = False
    is_in_minisite = False

    def update(self):
        super(LogoViewlet, self).update()
        self.root = api.portal.get_navigation_root(self.context)
        logo_field = None
        if IImioSmartwebMinisite.providedBy(self.root):
            self.update_minisite()
            logo_field = self.root.logo
            data = getattr(logo_field, "data", None)
            filename = getattr(logo_field, "filename", None)
        else:
            registry = getUtility(IRegistry)
            settings = registry.forInterface(ISiteSchema, prefix="plone")
            if getattr(settings, "site_logo", False):
                logo_field = settings.site_logo
                filename, data = b64decode_file(logo_field)
        if not self.show_logo or not logo_field:
            return
        if is_svg(filename):
            self.is_svg = True
            self.svg_data = data

    def update_minisite(self):
        minisite = self.root
        self.is_in_minisite = True
        if minisite.logo is None:
            self.show_logo = False
        else:
            self.show_logo = minisite.logo_display_mode in ["logo", "logo_title"]
            self.img_src = get_scale_url(minisite, self.request, "logo", "preview")
        self.show_title = minisite.logo_display_mode in ["title", "logo_title"]
        self.logo_title = self.navigation_root_title
