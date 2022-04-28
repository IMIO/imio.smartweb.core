# -*- coding: utf-8 -*-

from imio.smartweb.core.behaviors.minisite import IImioSmartwebMinisite
from imio.smartweb.core.behaviors.subsite import IImioSmartwebSubsite
from plone import api
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.layout.viewlets import common
from Products.CMFPlone.utils import parent


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

    def update(self):
        if not self.available():
            return
        self.sections = self.footer.listFolderContents()


class FooterViewlet(BaseFooterViewlet):
    css_id = "smartweb-footer"

    @property
    def footer(self):
        if self._footer is not None:
            return self._footer
        root = api.portal.get_navigation_root(self.context)
        if IImioSmartwebMinisite.providedBy(root):
            # don't display portal footer in a minisite
            return
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
        while not INavigationRoot.providedBy(obj):
            if IImioSmartwebSubsite.providedBy(obj):
                footers = obj.listFolderContents(
                    contentFilter={"portal_type": "imio.smartweb.Footer"}
                )
                if len(footers) > 0:
                    self._footer = footers[0]
                    return self._footer
            obj = parent(obj)


class MinisiteFooterViewlet(BaseFooterViewlet):
    css_id = "smartweb-minisite-footer"

    @property
    def footer(self):
        if self._footer is not None:
            return self._footer
        root = api.portal.get_navigation_root(self.context)
        if IImioSmartwebMinisite.providedBy(root):
            footers = root.listFolderContents(
                contentFilter={"portal_type": "imio.smartweb.Footer"}
            )
            if len(footers) > 0:
                self._footer = footers[0]
                return self._footer
