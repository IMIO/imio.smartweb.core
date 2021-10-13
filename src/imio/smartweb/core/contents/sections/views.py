# -*- coding: utf-8 -*-

from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from plone.locking.browser.info import LockInfoViewlet
from Products.CMFPlone.utils import normalizeString
from Products.Five.browser import BrowserView
from zope.interface import Interface


class ISectionView(Interface):
    """ """


class SectionView(BrowserView):
    """Section view"""

    def __call__(self):
        self.redirect_to_section(self.context.id)

    def locking_info(self):
        return LockInfoViewlet(self.context, self.request, None, None).render()

    def redirect_to_section(self, section_id):
        page = self.context.aq_parent
        url = "{}#section-{}".format(page.absolute_url(), section_id)
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
        api.portal.show_message(_("Section title has been hidden"), self.request)
        self.redirect_to_section(self.context.id)

    def show_section_title(self):
        if not self.context.can_toggle_title_visibility:
            return
        self.context.hide_title = False
        api.portal.show_message(_("Section title has been shown"), self.request)
        self.redirect_to_section(self.context.id)

    def item_url(self, item):
        if hasattr(self.context, "linking_rest_view"):
            """For sections events, news, contact, url is insite linking rest view"""
            linking_view_url = self.context.linking_rest_view.to_object.absolute_url()
            return f"{linking_view_url}/{normalizeString(self.context.Title())}/{self.context.UID()}"
        else:
            return item["url"]
