# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import common
from Products.CMFPlone.utils import base_hasattr


class BannerViewlet(common.ViewletBase):
    _banner_item = None

    def available(self):
        return self.banner_item and self.banner_item.banner

    @property
    def banner_item(self):
        if self._banner_item is not None:
            return self._banner_item
        for item in self.context.aq_chain:
            if base_hasattr(item, "banner") and item.banner is not None:
                self._banner_item = item
                return item

    def background_style(self):
        css_bg_image = "background-image:url('{}/@@images/banner/large');"
        css_bg_image = css_bg_image.format(self.banner_item.absolute_url())
        css_bg_size = "background-size:cover;"
        return " ".join([css_bg_image, css_bg_size])
