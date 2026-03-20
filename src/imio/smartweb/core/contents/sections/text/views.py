# -*- coding: utf-8 -*-

from imio.smartweb.core.utils import get_scale_url
from imio.smartweb.core.contents.sections.views import SectionView


class TextView(SectionView):
    """Gallery Section view"""

    def get_scale_url(self, item):
        return get_scale_url(item, self.request, "image", "section_text")
