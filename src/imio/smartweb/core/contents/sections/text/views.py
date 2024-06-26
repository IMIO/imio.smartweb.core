# -*- coding: utf-8 -*-

from imio.smartweb.core.utils import get_scale_url
from imio.smartweb.core.contents.sections.views import SectionView


class TextView(SectionView):
    """Gallery Section view"""

    def get_scale_url(self, item):
        request = self.request
        scale = self.context.image_size
        if self.context.image._height > self.context.image._width:
            return get_scale_url(item, request, "image", scale, "portrait")
        return get_scale_url(item, request, "image", scale, "paysage")
