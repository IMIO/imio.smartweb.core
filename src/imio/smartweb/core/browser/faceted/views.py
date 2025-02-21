# -*- coding: utf-8 -*-

from eea.facetednavigation.browser.app.view import FacetedContainerView
from eea.facetednavigation.layout.interfaces import IFacetedLayout
from imio.smartweb.core.interfaces import IViewWithoutLeadImage
from imio.smartweb.core.utils import get_scale_url
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from plone.app.contenttypes.browser.folder import FolderView
from plone.app.contenttypes.interfaces import IFile
from zope.component import queryAdapter
from zope.i18n import translate
from zope.interface import implementer


@implementer(IViewWithoutLeadImage)
class SmartwebFacetedContainerView(FacetedContainerView):
    """Faceted view without lead image"""


class FacetedView(FolderView):
    """Faceted common view"""

    @property
    def layout(self):
        context = self.context
        current_layout = queryAdapter(context, IFacetedLayout).layout
        return current_layout

    def show_images(self):
        return "with-images" in self.layout

    def is_video(self, item):
        return item.portal_type == "imio.smartweb.SectionVideo"

    def is_target_blank(self, item):
        # don't wake up object
        if item.portal_type == "File":
            return True
        # if IFile.providedBy(item.getObject()):
        #     return True
        return False

    def target(self, item):
        if self.is_target_blank(item):
            return "_blank"
        return ""

    def a_tag_item_title(self, item):
        title = item.Title or ""
        if self.is_target_blank(item):
            current_lang = api.portal.get_current_language()[:2]
            new_tab_txt = translate(_("New tab"), target_language=current_lang)
            return f"{title} ({new_tab_txt})"
        return title

    def get_scale_url(self, item, scale="vignette"):
        orientation = self.context.orientation
        if item.portal_type == "imio.smartweb.SectionGallery":
            images = item.getObject().listFolderContents()
            if not images:
                return ""
            scale_url = get_scale_url(
                images[0], self.request, "image", scale, orientation
            )
            return scale_url
        return get_scale_url(item, self.request, "image", scale, orientation)
