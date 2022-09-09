# -*- coding: utf-8 -*-

from Acquisition import aq_parent
from imio.smartweb.core.contents import IFolder
from imio.smartweb.core.utils import get_default_content_id
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from plone.app.layout.navigation.interfaces import INavigationRoot
from Products.CMFPlone.interfaces.constrains import DISABLED
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from Products.Five.browser import BrowserView


class HeroBannerSettings(BrowserView):
    """HeroBanner settings"""

    def add_herobanner(self):
        if not self.available():
            api.portal.show_message(
                _("Hero banner cannot be added here"), self.request, type="error"
            )
            self.request.response.redirect(self.context.absolute_url())
            return ""
        obj = self.context
        if not INavigationRoot.providedBy(obj):
            obj = aq_parent(obj)
        if IFolder.providedBy(obj):
            container = ISelectableConstrainTypes(obj)
            constrain_types_mode = container.getConstrainTypesMode()
            container.setConstrainTypesMode(DISABLED)
        pt = api.portal.get_tool("portal_types")
        portal_type = obj.portal_type
        allowed_content_types = pt.getTypeInfo(portal_type).allowed_content_types
        allowed_content_types = list(allowed_content_types)
        allowed_content_types.append("imio.smartweb.HeroBanner")
        pt.getTypeInfo(portal_type).allowed_content_types = tuple(allowed_content_types)
        herobanner = api.content.create(
            title=_("Hero banner"),
            id="herobanner",
            container=obj,
            type="imio.smartweb.HeroBanner",
        )
        herobanner.exclude_from_parent_listing = True
        herobanner.reindexObject(idxs=["exclude_from_parent_listing"])
        allowed_content_types.remove("imio.smartweb.HeroBanner")
        pt.getTypeInfo(portal_type).allowed_content_types = tuple(allowed_content_types)
        if IFolder.providedBy(obj):
            container.setConstrainTypesMode(constrain_types_mode)
        api.portal.show_message(
            _("Hero banner has been successfully added"), self.request
        )
        self.request.response.redirect(herobanner.absolute_url())

    def available(self):
        obj = self.context
        if not INavigationRoot.providedBy(obj):
            parent = aq_parent(obj)
            if not INavigationRoot.providedBy(parent):
                return False

            default_page_id = get_default_content_id(parent)
            if default_page_id == obj.id:
                obj = parent
            else:
                return False

        herobanners = obj.listFolderContents(
            contentFilter={"portal_type": "imio.smartweb.HeroBanner"}
        )
        return len(herobanners) == 0
