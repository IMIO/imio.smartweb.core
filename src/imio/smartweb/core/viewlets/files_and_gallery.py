# -*- coding: utf-8 -*-

from collective.behavior.gallery.viewlets.gallery import GalleryViewlet
from imio.smartweb.core.behaviors.page import IPageSections
from plone.app.layout.viewlets import ViewletBase
from zope.component import queryMultiAdapter


class FilteredGalleryViewlet(GalleryViewlet):
    """ A viewlet which renders the filtered gallery """

    def available(self):
        return (
            IPageSections.providedBy(self.context)
            and "images" in self.context.visible_sections
        )

    def get_photos(self):
        if not self.available():
            return []
        return [item.to_object for item in self.context.selected_images]


class FilteredFilesViewlet(ViewletBase):
    """ A viewlet which renders the filtered files """

    def available(self):
        return (
            IPageSections.providedBy(self.context)
            and "files" in self.context.visible_sections
        )

    def get_files(self):
        return [item.to_object for item in self.context.selected_files]

    def get_thumb_scale_list(self):
        view = queryMultiAdapter((self.context, self.request), name="listing_view")
        return "tile"
        return view.get_thumb_scale_list()

    def get_mime_type_icon(self, file_obj):
        view = queryMultiAdapter((self.context, self.request), name="contenttype_utils")
        return view.getMimeTypeIcon(file_obj.file)
