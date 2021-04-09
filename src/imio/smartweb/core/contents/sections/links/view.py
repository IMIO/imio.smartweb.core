# -*- coding: utf-8 -*-

from zope.component import queryMultiAdapter
from imio.smartweb.core.contents.sections.views import SectionView


class LinksView(SectionView):
    """Links Section view"""

    def get_thumb_scale_list(self):
        view = queryMultiAdapter((self.context, self.request), name="listing_view")
        return view.get_thumb_scale_list()
