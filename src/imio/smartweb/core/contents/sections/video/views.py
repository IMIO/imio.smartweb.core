# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.embedder import get_video_embedder
from imio.smartweb.core.contents.sections.views import SectionView


class VideoView(SectionView):
    def get_embed_video(self, width=800, height=600):
        embedder = get_video_embedder(width=width, height=height)
        return embedder(self.context.video_url, params=dict(autoplay=False))
