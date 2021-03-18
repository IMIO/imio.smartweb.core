# -*- coding: utf-8 -*-

from plone.gallery.views.photo_gallery import PhotoGallery
from imio.smartweb.core.contents.sections.views import SectionView


class GalleryView(SectionView, PhotoGallery):
    """Gallery Section view"""
