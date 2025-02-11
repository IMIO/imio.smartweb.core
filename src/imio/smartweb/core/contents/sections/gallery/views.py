# -*- coding: utf-8 -*-

from plone.gallery.views.photo_gallery import PhotoGallery
from imio.smartweb.core.utils import get_scale_url
from imio.smartweb.core.contents.sections.views import SectionView


class GalleryView(SectionView, PhotoGallery):
    """Gallery Section view"""

    def get_scale_url(self, item, scale, orientation="paysage"):
        request = self.request
        return get_scale_url(item, request, "image", scale, orientation)

    def alt_label(self, item):
        title = item.title or ""
        description = item.description or ""
        # Accessibility: if title is the same as the filename, return empty string because, filename is not a good practice in alt tag for an img.
        if item.image and title == item.image.filename and len(description) == 0:
            title = ""
        # Accessibility : Return description if longer is same or greater than title.
        if len(description) >= len(title):
            return description
        return title
