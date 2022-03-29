# -*- coding: utf-8 -*-

from imio.smartweb.core.behaviors.subsite import IImioSmartwebSubsite
from imio.smartweb.core.contents import IFolder
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from plone.app.layout.navigation.interfaces import INavigationRoot
from Products.CMFPlone.interfaces.constrains import DISABLED
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from Products.Five.browser import BrowserView


class HeroBannerSettings(BrowserView):
    """HeroBanner settings"""

    def add_herobanner(self):
        if not self.available:
            api.portal.show_message(
                _("Hero banner cannot be added here"), self.request, type="error"
            )
            self.request.response.redirect(self.context.absolute_url())
            return ""
        if IFolder.providedBy(self.context):
            container = ISelectableConstrainTypes(self.context)
            constrain_types_mode = container.getConstrainTypesMode()
            container.setConstrainTypesMode(DISABLED)
        pt = api.portal.get_tool("portal_types")
        portal_type = self.context.portal_type
        allowed_content_types = pt.getTypeInfo(portal_type).allowed_content_types
        allowed_content_types = list(allowed_content_types)
        allowed_content_types.append("imio.smartweb.HeroBanner")
        pt.getTypeInfo(portal_type).allowed_content_types = tuple(allowed_content_types)
        herobanner = api.content.create(
            title=_("Hero banner"),
            id="herobanner",
            container=self.context,
            type="imio.smartweb.HeroBanner",
        )
        herobanner.exclude_from_parent_listing = True
        herobanner.reindexObject(idxs=("exclude_from_parent_listing"))
        allowed_content_types.remove("imio.smartweb.HeroBanner")
        pt.getTypeInfo(portal_type).allowed_content_types = tuple(allowed_content_types)
        if IFolder.providedBy(self.context):
            container.setConstrainTypesMode(constrain_types_mode)
        api.portal.show_message(
            _("Hero banner has been successfully added"), self.request
        )
        self.request.response.redirect(herobanner.absolute_url())

    @property
    def available(self):
        if not INavigationRoot.providedBy(self.context):
            return False
        herobanners = self.context.listFolderContents(
            contentFilter={"portal_type": "imio.smartweb.HeroBanner"}
        )
        return len(herobanners) == 0
