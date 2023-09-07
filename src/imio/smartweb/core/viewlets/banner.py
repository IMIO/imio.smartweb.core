# -*- coding: utf-8 -*-

from imio.smartweb.core.browser.banner.settings import ILocallyHiddenBanner
from imio.smartweb.core.utils import hash_md5
from plone import api
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.layout.viewlets import common
from plone.namedfile.file import NamedBlobImage
from Products.CMFPlone.utils import base_hasattr


class BannerViewlet(common.ViewletBase):
    _banner_item = None
    _banner_is_hidden = False

    def available(self):
        if self.banner_item is None:
            # There is no banner defined in parents
            return False
        elif self.is_banner_hidden and not self.is_banner_locally_hidden:
            # Banner is hidden in a parent content
            return False
        can_edit = api.user.has_permission("Modify portal content", obj=self.context)
        if self.is_banner_locally_hidden and not can_edit:
            # Banner is hidden locally, but user can not edit its display
            return False
        return True

    @property
    def banner_item(self):
        if self._banner_item is not None:
            return self._banner_item
        for item in self.context.aq_chain:
            if ILocallyHiddenBanner.providedBy(item):
                self._banner_is_hidden = True
            if (
                base_hasattr(item, "banner")
                and item.banner is not None
                and isinstance(item.banner, NamedBlobImage)
            ):
                self._banner_item = item
                return item
            if INavigationRoot.providedBy(item):
                return

    @property
    def is_banner_hidden(self):
        return self.banner_item and self._banner_is_hidden

    @property
    def is_banner_locally_hidden(self):
        return ILocallyHiddenBanner.providedBy(self.context)

    def background_style(self):
        if self.is_banner_hidden:
            return ""
        modification_date = self.banner_item.ModificationDate()
        modified_hash = hash_md5(modification_date)
        image_url = f"{self.banner_item.absolute_url()}/@@images/banner?cache_key={modified_hash}"
        css_bg_image = f"background-image:url({image_url});"
        css_bg_size = "background-size:cover;"
        return " ".join([css_bg_image, css_bg_size])
