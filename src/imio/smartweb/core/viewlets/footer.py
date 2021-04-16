# -*- coding: utf-8 -*-

from Acquisition import aq_base
from Acquisition import aq_inner
from Acquisition import aq_parent
from imio.smartweb.core.behaviors.subsite import IImioSmartwebSubsite
from plone import api
from plone.app.layout.viewlets import common


class BaseFooterViewlet(common.ViewletBase):
    _footer = None

    def available(self):
        return self.footer is not None

    def background_style(self):
        footer = self.footer
        if not footer.background_image:
            return ""
        css_bg_image = "background-image:url('{}/@@images/background_image/large');"
        css_bg_image = css_bg_image.format(footer.absolute_url())
        css_bg_size = "background-size:cover;"
        return " ".join([css_bg_image, css_bg_size])


class FooterViewlet(BaseFooterViewlet):
    css_id = "smartweb-footer"

    @property
    def footer(self):
        if self._footer is not None:
            return self._footer
        portal = api.portal.get()
        footers = portal.listFolderContents(
            contentFilter={"portal_type": "imio.smartweb.Footer"}
        )
        if len(footers) > 0:
            self._footer = footers[0]
            return self._footer


class SubsiteFooterViewlet(BaseFooterViewlet):
    css_id = "smartweb-subsite-footer"

    @property
    def footer(self):
        if self._footer is not None:
            return self._footer
        obj = self.context
        portal = api.portal.get()
        while aq_base(obj) is not aq_base(portal):
            if IImioSmartwebSubsite.providedBy(obj):
                footers = obj.listFolderContents(
                    contentFilter={"portal_type": "imio.smartweb.Footer"}
                )
                if len(footers) > 0:
                    self._footer = footers[0]
                    return self._footer
            parent = aq_parent(aq_inner(obj))
            obj = parent
