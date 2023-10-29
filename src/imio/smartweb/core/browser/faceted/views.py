# -*- coding: utf-8 -*-

from eea.facetednavigation.browser.app.view import FacetedContainerView
from eea.facetednavigation.layout.interfaces import IFacetedLayout
from imio.smartweb.core.interfaces import IViewWithoutLeadImage
from imio.smartweb.core.utils import get_scale_url
from plone.app.contenttypes.browser.folder import FolderView
from zope.component import queryAdapter
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
