# -*- coding: utf-8 -*-

from eea.facetednavigation.browser.app.view import FacetedContainerView
from eea.facetednavigation.layout.interfaces import IFacetedLayout
from imio.smartweb.core.interfaces import IViewWithoutLeadImage
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

    def get_image_url(self, item):
        if item.portal_type == "imio.smartweb.SectionGallery":
            images = item.getObject().listFolderContents()
            if not images:
                return ""
            url = images[0].absolute_url()
            return f"{url}/@@images/image"
        if not item.has_leadimage:
            return ""
        url = item.getURL()
        return f"{url}/@@images/image"
