# -*- coding: utf-8 -*-

from embeddify import Embedder
from embeddify import Plugin
from imio.smartweb.core.contents.sections.views import SectionView
from imio.smartweb.locales import SmartwebMessageFactory as _
from json.decoder import JSONDecodeError

import json


class ExternalContentView(SectionView):
    def get_embed_external_content(self, width="100%", height=600):
        plugins = [EaglebePlugin(), EllohaPlugin(), UnknowServicePlugin()]
        extra_params = self.context.external_content_params
        plugin_config = {
            "eaglebeplugin": {"width": width},
            "ellohaplugin": {"width": width, "extra_params": extra_params},
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


class EllohaPlugin(Plugin):
    def __call__(self, parts, config={}):
        if "reservation.elloha.com" in parts.netloc:
            # sample :
            # {
            #     "ConstellationWidgetContainer": "917c4c52-c997-4077-9135-873a0b2e0c85",
            #     "Idoi": "195ea849-1732-4a69-a051-e7911001cd09"
            # }
            extra_params = config["extra_params"]
            error_message = '<div class="elloha">With an elloha plugin, extra params must contain a dictionary with two keys : ConstellationWidgetContainer, Idoi</div>'

            if (
                extra_params is None
                or extra_params[0] != "{"
                or extra_params[-1] != "}"
            ):
                return error_message
            try:
                res = json.loads(extra_params.lower())
            except JSONDecodeError:
                return error_message

            if (
                res.get("constellationwidgetcontainer") is None
                or res.get("idoi") is None
            ):
                return error_message

            cw1 = res.get("constellationwidgetcontainer")
            cw2 = cw1.replace("-", "")
            idoi = res.get("idoi")
            return (
                f'<div class="elloha">'
                f'<div id="ConstellationWidgetContainer{cw1}" '
                f'style="width:100%" data-id-projet="{cw2}">...</div></div>'
                f'<script type="text/javascript" src="{parts.geturl()}/Scripts/widget-loader.min.js?v=42"></script>'
                f'<script type="text/javascript">var constellationWidgetUrl{cw2}, '
                f"constellationTypeModule{cw2};"
                f'constellationWidgetUrl{cw2} = "https://reservation.elloha.com/Widget/BookingEngine/{cw1}?idoi={idoi}&culture=fr-FR";'
                f'constellationTypeModule{cw2}=1; constellationWidgetLoad("ConstellationWidgetContainer{cw1}");'
                f'constellationWidgetAddEvent(window, "resize", function () {{constellationWidgetSetAppearance("ConstellationWidgetContainer{cw1}");}});</script>'
            )
        #
        return None


class UnknowServicePlugin(Plugin):
    def __call__(self, parts, config={}):
        return _("<p class='unknow_service'>Unknow service</p>")
