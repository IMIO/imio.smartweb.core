# -*- coding: utf-8 -*-

from zope.component import queryMultiAdapter
from imio.smartweb.core.contents.sections.views import SectionView


class FilesView(SectionView):
    """ A viewlet which renders the filtered files """

    def get_thumb_scale_list(self):
        view = queryMultiAdapter((self.context, self.request), name="listing_view")
        # return "tile"
        return view.get_thumb_scale_list()

    def get_mime_type_icon(self, file_obj):
        view = queryMultiAdapter((self.context, self.request), name="contenttype_utils")
        return view.getMimeTypeIcon(file_obj.file)
