# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.views import SectionView
from Products.CMFPlone.interfaces import ISiteSchema
from Products.CMFPlone.utils import human_readable_size
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.component import queryMultiAdapter


class FilesView(SectionView):
    """Files Section view"""

    def get_thumb_scale(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISiteSchema, prefix="plone", check=False)
        if settings.no_thumbs_lists:
            return None
        return settings.thumb_scale_listing

    def get_mime_type_icon(self, file_obj):
        view = queryMultiAdapter((self.context, self.request), name="contenttype_utils")
        return view.getMimeTypeIcon(file_obj.file)

    def human_readable_size(self, file_obj):
        return human_readable_size(file_obj.file.getSize())
