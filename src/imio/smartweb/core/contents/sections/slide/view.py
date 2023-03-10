# -*- coding: utf-8 -*-

from embeddify import Embedder
from imio.smartweb.core.contents.sections.views import SectionView
from imio.smartweb.core.utils import get_scale_url
from plone.app.contenttypes.utils import replace_link_variables_by_paths


class SlideView(SectionView):
    """Selection Section view"""

    def get_embed_video(self, width=800, height=600):
        embedder = Embedder(width=width, height=height)
        return embedder(self.context.video_url, params=dict(autoplay=True))

    def get_scale_url(self):
        context = self.context
        request = self.request
        return get_scale_url(context, request, "image", "banner")

    def link(self):
        context = self.context
        return replace_link_variables_by_paths(context, context.remoteUrl)
