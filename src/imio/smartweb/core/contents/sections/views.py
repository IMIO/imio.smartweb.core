# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from zope.interface import Interface


class ISectionView(Interface):
    """"""


class SectionView(BrowserView):
    """Section view"""

    def __call__(self):
        page = self.context.aq_parent
        url = "{}#{}".format(page.absolute_url(), self.context.id)
        return self.request.response.redirect(url)

    def background_style(self):
        if not self.context.background_image:
            return ""
        css_bg_image = "background-image:url('{}/@@images/background_image/large');"
        css_bg_image = css_bg_image.format(self.context.absolute_url())
        css_bg_size = "background-size:cover;"
        return " ".join([css_bg_image, css_bg_size])
