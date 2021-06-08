# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from Acquisition import aq_parent
from imio.smartweb.core.behaviors.subsite import IImioSmartwebSubsite
from plone import api
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.layout.viewlets import common
from zope.component import getMultiAdapter


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

    def sections(self):
        # we don't want to show edition tools in footer sections
        self.request.set("can_edit", False)
        sections = self.footer.listFolderContents()
        for section in sections:
            view = getMultiAdapter((section, self.request), name="full_view_item")
            yield view()


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
        while not INavigationRoot.providedBy(obj):
            if IImioSmartwebSubsite.providedBy(obj):
                footers = obj.listFolderContents(
                    contentFilter={"portal_type": "imio.smartweb.Footer"}
                )
                if len(footers) > 0:
                    self._footer = footers[0]
                    return self._footer
            parent = aq_parent(aq_inner(obj))
            obj = parent
