# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.views import SectionView
from plone.app.contenttypes.browser.folder import FolderView
from Products.CMFPlone.utils import human_readable_size
from zope.component import queryMultiAdapter


class FilesView(SectionView, FolderView):
    """Files Section view"""

    def get_mime_type_icon(self, file_obj):
        view = queryMultiAdapter((self.context, self.request), name="contenttype_utils")
        return view.getMimeTypeIcon(file_obj.file)

    def human_readable_size(self, file_obj):
        return human_readable_size(file_obj.file.getSize())
