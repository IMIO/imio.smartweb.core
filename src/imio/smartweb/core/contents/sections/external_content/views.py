# -*- coding: utf-8 -*-

from embeddify import Embedder
from embeddify import Plugin
from imio.smartweb.core.contents.sections.views import SectionView
from imio.smartweb.core.interfaces import IArcgisViewUtils
from imio.smartweb.locales import SmartwebMessageFactory as _
from json.decoder import JSONDecodeError
from plone import api
from plone.app.contenttypes.behaviors.leadimage import ILeadImage
from Products.Five.browser import BrowserView
from zope.i18n import translate
from zope.interface import implementer

import json


class ExternalContentView(SectionView):
    def get_embed_external_content(self, width="100%", height=600):
        current_lang = api.portal.get_current_language()[:2]
        plugins = [
            EaglebePlugin(),
            EllohaPlugin(),
            CognitoformPlugin(),
            ArcgisPlugin(),
            GiveADayPlugin(),
            UnknowServicePlugin(),
        ]
        extra_params = self.context.external_content_params
        plugin_config = {
            "eaglebeplugin": {"width": width},
            "ellohaplugin": {
                "width": width,
                "current_lang": current_lang,
                "extra_params": extra_params,
            },
            "cognitoformplugin": {
                "width": width,
                "current_lang": current_lang,
                "extra_params": extra_params,
            },
            "arcgisplugin": {
                "width": width,
                "url": self.context.absolute_url(),
                "current_lang": current_lang,
                "extra_params": extra_params,
            },
            "giveadayplugin": {},
            "unknowserviceplugin": {"width": width, "current_lang": current_lang},
        }
        embedder = Embedder(plugins=plugins, plugin_config=plugin_config)
        url = self.context.external_content_url
        return embedder(url, config={"width": width})

    def has_leadimage(self):
        if ILeadImage.providedBy(self.context) and getattr(
            self.context, "image", False
        ):
            return True
        return False

    def image(self):
        return f"{self.context.absolute_url()}/@@download/image"


class EaglebePlugin(Plugin):
    def __call__(self, parts, config={}):
        return None

        # if "app.eaglebe.com" in parts.netloc:
        #    return f'<iframe class="eaglebe" src="{parts.geturl()}" scrolling="no" width="{config["width"]}">'


class EllohaPlugin(Plugin):
    def __call__(self, parts, config={}):
        if "reservation.elloha.com" in parts.netloc:
            # sample :
            # {
            #     "ConstellationWidgetContainer": "917c4c52-c997-4077-9135-873a0b2e0c85",
            #     "Idoi": "195ea849-1732-4a69-a051-e7911001cd09"
            # }
            current_lang = config["current_lang"]
            extra_params = config["extra_params"]

            error_message = _(
                "With an elloha plugin, extra params must contain a dictionary with two keys : ConstellationWidgetContainer, Idoi"
            )
            error_message = translate(error_message, target_language=current_lang)
            error_message = f'<div class="elloha elloha_error">{error_message}</div>'

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


class CognitoformPlugin(Plugin):
    def __call__(self, parts, config={}):
        if "cognitoforms" in parts.netloc:
            current_lang = config["current_lang"]
            extra_params = config["extra_params"]

            error_message = _(
                "With a cognitoform plugin, extra params can be void but if you complete it you must specify : scrolling:(yes/no) and overflow:(hidden/scroll/auto)"
            )
            error_message = translate(error_message, target_language=current_lang)
            error_message = (
                f'<div class="cognitoform cognitoform_error">{error_message}</div>'
            )

            if extra_params is None:
                return f'<iframe src="{parts.geturl()}" style="border: 0px none; width: {config["width"]}%; overflow: auto;" scrolling="yes"></iframe>'
            else:
                if extra_params[0] != "{" or extra_params[-1] != "}":
                    return error_message
                try:
                    res = json.loads(extra_params.lower())
                except JSONDecodeError:
                    return error_message

                if res.get("overflow") is None or res.get("scrolling") is None:
                    return error_message

                overflow = res.get("overflow")
                scrolling = res.get("scrolling")
                return f'<iframe src="{parts.geturl()}" style="border: 0px none; width: {config["width"]}%; overflow: {overflow};" scrolling="{scrolling}"></iframe>'
        #
        return None


class ArcgisPlugin(Plugin):
    def __call__(self, parts, config={}):
        if "arcgis" in parts.netloc:
            # url : https://developers.arcgis.com/
            # extra_params : {"portal_item_id":"27a432b0835149e6acd3ac39d0e4349c"}
            current_lang = config["current_lang"]
            extra_params = config["extra_params"]
            url = config["url"]

            error_message = _(
                "With arcgis plugin, extra params must contain a dictionary with one key : portal_item_id"
            )
            error_message = translate(error_message, target_language=current_lang)
            error_message = f'<div class="arcgis arcgis_error">{error_message}</div>'

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
            if res.get("portal_item_id") is None:
                return error_message

            portal_item_id = res.get("portal_item_id")
            msg = _("Consult the map")
            msg = translate(msg, target_language=current_lang)
            return (
                f'<a href="{url}/view_arcgis?portal_item_id={portal_item_id}">{msg}</a>'
            )
        #
        return None


class GiveADayPlugin(Plugin):
    def __call__(self, parts, config={}):
        if "www.giveaday.be" in parts.netloc:
            return (
                '<div id="giveaday-widget"></div>'
                "<script src=https://www.giveaday.be/assets/giveaday_v1.js></script>"
                "<script>"
                "function renderWidget() {"
                'giveADayWidget.initialize("giveaday-widget", 2924, "organization", "large", "fr","#34B78F");}'
                "renderWidget();"
                "</script>"
            )
        #
        return None


class UnknowServicePlugin(Plugin):
    def __call__(self, parts, config={}):
        current_lang = config["current_lang"]
        msg = _("Unknow service")
        msg = translate(msg, target_language=current_lang)
        return f'<p class="unknow_service">{msg}</p>'


@implementer(IArcgisViewUtils)
class ArcgisView(BrowserView):
    _footer = None

    @property
    def get_portal_item_id(self):
        return self.request.portal_item_id
