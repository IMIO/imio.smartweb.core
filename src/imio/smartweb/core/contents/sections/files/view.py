# -*- coding: utf-8 -*-

from zope.component import queryMultiAdapter
from imio.smartweb.core.contents.sections.views import SectionView
from Products.CMFPlone.utils import human_readable_size


class FilesView(SectionView):
    """ Files Section view """

    def get_thumb_scale_list(self):
        view = queryMultiAdapter((self.context, self.request), name="listing_view")
        # return "tile"
        return view.get_thumb_scale_list()

    def get_mime_type_icon(self, file_obj):
        view = queryMultiAdapter((self.context, self.request), name="contenttype_utils")
        return view.getMimeTypeIcon(file_obj.file)

    def human_readable_size(self, file_obj):
        return human_readable_size(file_obj.file.getSize())
