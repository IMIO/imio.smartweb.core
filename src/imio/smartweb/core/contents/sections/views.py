# -*- coding: utf-8 -*-

from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from plone.locking.browser.info import LockInfoViewlet
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


class CarouselOrTableSectionView(SectionView):
    """Section view that can display a carousel"""

    @property
    def image_scale(self):
        layout = self.context.getLayout()
        if layout == "carousel_view":
            # scale used depends on the batch size
            return self.context.nb_results_by_batch == 1 and "slide" or "vignette"
        elif layout == "table_view":
            return "vignette"
        else:
            return getattr(self.context, "image_scale", "")
