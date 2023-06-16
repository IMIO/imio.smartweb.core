# -*- coding: utf-8 -*-

from embeddify import Embedder
from embeddify import Plugin
from imio.smartweb.core.contents.sections.views import SectionView
from imio.smartweb.locales import SmartwebMessageFactory as _


class ExternalContentView(SectionView):
    def get_embed_external_content(self, width="100%", height=600):
        plugins = [EaglebePlugin(), UnknowServicePlugin()]
        plugin_config = {
            "eaglebeplugin": {"width": width},
            "unknowserviceplugin": {"width": width},
        }
        embedder = Embedder(plugins=plugins, plugin_config=plugin_config)
        url = self.context.external_content_url
        return embedder(url, config={"width": width})


class EaglebePlugin(Plugin):
    def __call__(self, parts, config={}):
        if "app.eaglebe.com" in parts.netloc:
            return f'<iframe class="eaglebe" src="{parts.geturl()}" scrolling="no" width="{config["width"]}">'
        #
        return None


class UnknowServicePlugin(Plugin):
    def __call__(self, parts, config={}):
        return _("<p class='unknow_service'>Unknow service</p>")
