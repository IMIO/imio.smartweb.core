# -*- coding: utf-8 -*-

from plone.gallery.views.photo_gallery import PhotoGallery
from imio.smartweb.core.utils import get_scale_url
from imio.smartweb.core.contents.sections.views import SectionView


class GalleryView(SectionView, PhotoGallery):
    """Gallery Section view"""

    def get_scale_url(self, item, scale, orientation="paysage"):
        request = self.request
        return get_scale_url(item, request, "image", scale, orientation)
