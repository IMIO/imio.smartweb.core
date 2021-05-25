# -*- coding: utf-8 -*-

from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from Products.Five.browser import BrowserView
from zope.interface import Interface


class ISectionView(Interface):
    """ """


class SectionView(BrowserView):
    """Section view"""

    def __call__(self):
        self.redirect_to_section(self.context.id)

    def redirect_to_section(self, section_id):
        page = self.context.aq_parent
        url = "{}#{}".format(page.absolute_url(), section_id)
        self.request.response.redirect(url)

    def background_style(self):
        if not self.context.background_image:
            return ""
        css_bg_image = "background-image:url('{}/@@images/background_image/large');"
        css_bg_image = css_bg_image.format(self.context.absolute_url())
        css_bg_size = "background-size:cover;"
        return " ".join([css_bg_image, css_bg_size])

    def hide_section_title(self):
        if not self.context.can_toggle_title_visibility:
            return
        self.context.hide_title = True
        api.portal.show_message(_(u"Section title has been hidden"), self.request)
        self.redirect_to_section(self.context.id)

    def show_section_title(self):
        if not self.context.can_toggle_title_visibility:
            return
        self.context.hide_title = False
        api.portal.show_message(_(u"Section title has been shown"), self.request)
        self.redirect_to_section(self.context.id)
