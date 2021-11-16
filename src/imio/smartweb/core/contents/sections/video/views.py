# -*- coding: utf-8 -*-

from embeddify import Embedder
from imio.smartweb.core.contents.sections.views import SectionView


class VideoView(SectionView):
    def get_embed_video(self, width=800, height=600):
        embedder = Embedder(width=width, height=height)
        return embedder(self.context.video_url, params=dict(autoplay=False))
