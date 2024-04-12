# -*- coding: utf-8 -*-

from embeddify import Embedder
from embeddify import Plugin

from imio.smartweb.core.interfaces import IOdwbViewUtils
from imio.smartweb.core.contents.sections.views import SectionView
from imio.smartweb.core.interfaces import IArcgisViewUtils
from imio.smartweb.locales import SmartwebMessageFactory as _
from json.decoder import JSONDecodeError
from plone import api
from plone.app.contenttypes.behaviors.leadimage import ILeadImage
from Products.Five.browser import BrowserView
from zope.i18n import translate
from zope.interface import implementer
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

import json
import logging
import requests

logger = logging.getLogger("imio.smartweb.core")


class ExternalContentView(SectionView):

    plugin_config = {}

    def __init__(self, context, request):
        width = "100%"
        current_lang = api.portal.get_current_language()[:2]
        plugins = [
            EaglebePlugin(),
            EllohaPlugin(),
            CognitoformPlugin(),
            ArcgisPlugin(),
            GiveADayPlugin(),
            IdeluxWastePlugin(),
            InbwContainersAffluencePlugin(),
            OdwbWidgetPlugin(),
            UnknowServicePlugin(),
        ]
        extra_params = context.external_content_params
        self.plugin_config = {
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
                "url": context.absolute_url(),
                "current_lang": current_lang,
                "extra_params": extra_params,
            },
            "giveadayplugin": {},
            "ideluxwasteplugin": {
                "url": context.absolute_url(),
                "extra_params": extra_params,
            },
            "inbwcontainersaffluenceplugin": {
                "url": context.absolute_url(),
                "extra_params": extra_params,
            },
            "odwbwidgetplugin": {
                "url": context.absolute_url(),
                "extra_params": extra_params,
            },
            "unknowserviceplugin": {"width": width, "current_lang": current_lang},
        }
        embedder = Embedder(plugins=plugins, plugin_config=self.plugin_config)
        url = context.external_content_url
        self.plugin = embedder(url, config={"width": width})
        super(ExternalContentView, self).__init__(context, request)

    @property
    def contents(self):
        return self.plugin.contents

    def display_odwb_widget_viewlet(self):
        return self.plugin.is_odwb_widget_plugins

    def render_viewlet(self):
        return self.index()

    def has_leadimage(self):
        if ILeadImage.providedBy(self.context) and getattr(
            self.context, "image", False
        ):
            return True
        return False

    def get_plugin(self):
        return self.plugin

    def which_plugin(self):
        if IOdwbWidgetPlugin.providedBy(self.plugin):
            return "odwbwidgetplugin"
        elif IIdeluxWastePlugin.providedBy(self.plugin):
            return "ideluxwasteplugin"
        elif IInbwContainersAffluencePlugin.providedBy(self.plugin):
            return "inbwcontainersaffluenceplugin"
        else:
            return None

    def image(self):
        return f"{self.context.absolute_url()}/@@download/image"


class BasePlugin(Plugin):
    """ """

    is_odwb_widget_plugins = False

    @property
    def contents(self):
        return ""


class EaglebePlugin(BasePlugin):
    def __call__(self, parts, config={}):
        self.parts = parts
        self.config = config
        if "app.eaglebe.com" in parts.netloc:
            return self
        return None

    @property
    def contents(self):
        return f'<iframe class="eaglebe" src="{self.parts.geturl()}" scrolling="no" width="{self.config["width"]}">'


class EllohaPlugin(BasePlugin):
    def __call__(self, parts, config={}):
        if "reservation.elloha.com" in parts.netloc:
            self.parts = parts
            self.config = config
            return self
        return None

    @property
    def contents(self):
        # sample :
        # {
        #     "ConstellationWidgetContainer": "917c4c52-c997-4077-9135-873a0b2e0c85",
        #     "Idoi": "195ea849-1732-4a69-a051-e7911001cd09"
        # }
        current_lang = self.config["current_lang"]
        extra_params = self.config["extra_params"]
        error_message = _(
            "With an elloha plugin, extra params must contain a dictionary with two keys : ConstellationWidgetContainer, Idoi"
        )
        error_message = translate(error_message, target_language=current_lang)
        error_message = f'<div class="elloha elloha_error">{error_message}</div>'

        if extra_params is None or extra_params[0] != "{" or extra_params[-1] != "}":
            return error_message
        try:
            res = json.loads(extra_params.lower())
        except JSONDecodeError:
            return error_message

        if res.get("constellationwidgetcontainer") is None or res.get("idoi") is None:
            return error_message

        cw1 = res.get("constellationwidgetcontainer")
        cw2 = cw1.replace("-", "")
        idoi = res.get("idoi")
        return (
            f'<div class="elloha">'
            f'<div id="ConstellationWidgetContainer{cw1}" '
            f'style="width:100%" data-id-projet="{cw2}">...</div></div>'
            f'<script type="text/javascript" src="{self.parts.geturl()}/Scripts/widget-loader.min.js?v=42"></script>'
            f'<script type="text/javascript">var constellationWidgetUrl{cw2}, '
            f"constellationTypeModule{cw2};"
            f'constellationWidgetUrl{cw2} = "https://reservation.elloha.com/Widget/BookingEngine/{cw1}?idoi={idoi}&culture=fr-FR";'
            f'constellationTypeModule{cw2}=1; constellationWidgetLoad("ConstellationWidgetContainer{cw1}");'
            f'constellationWidgetAddEvent(window, "resize", function () {{constellationWidgetSetAppearance("ConstellationWidgetContainer{cw1}");}});</script>'
        )


class CognitoformPlugin(BasePlugin):
    def __call__(self, parts, config={}):
        if "cognitoforms" in parts.netloc:
            self.parts = parts
            self.config = config
            return self
        return None

    @property
    def contents(self):
        current_lang = self.config["current_lang"]
        extra_params = self.config["extra_params"]

        error_message = _(
            "With a cognitoform plugin, extra params can be void but if you complete it you must specify : scrolling:(yes/no) and overflow:(hidden/scroll/auto)"
        )
        error_message = translate(error_message, target_language=current_lang)
        error_message = (
            f'<div class="cognitoform cognitoform_error">{error_message}</div>'
        )

        if extra_params is None:
            return f'<iframe src="{self.parts.geturl()}" style="border: 0px none; width: {self.config["width"]}%; overflow: auto;" scrolling="yes"></iframe>'
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
            return f'<iframe src="{self.parts.geturl()}" style="border: 0px none; width: {self.config["width"]}%; overflow: {overflow};" scrolling="{scrolling}"></iframe>'


class ArcgisPlugin(BasePlugin):
    def __call__(self, parts, config={}):
        if "arcgis" in parts.netloc:
            self.parts = parts
            self.config = config
            return self
        return None

    @property
    def contents(self):
        # url : https://developers.arcgis.com/
        # extra_params : {"portal_item_id":"27a432b0835149e6acd3ac39d0e4349c"}
        current_lang = self.config["current_lang"]
        extra_params = self.config["extra_params"]
        url = self.config["url"]

        error_message = _(
            "With arcgis plugin, extra params must contain a dictionary with one key : portal_item_id"
        )
        error_message = translate(error_message, target_language=current_lang)
        error_message = f'<div class="arcgis arcgis_error">{error_message}</div>'

        if extra_params is None or extra_params[0] != "{" or extra_params[-1] != "}":
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
        return f'<a href="{url}/view_arcgis?portal_item_id={portal_item_id}">{msg}</a>'


class GiveADayPlugin(BasePlugin):
    def __call__(self, parts, config={}):
        if "www.giveaday.be" in parts.netloc:
            self.parts = parts
            self.config = config
            return self
        #
        return None

    @property
    def contents(self):
        return (
            '<div id="giveaday-widget"></div>'
            "<script src=https://www.giveaday.be/assets/giveaday_v1.js></script>"
            "<script>"
            "function renderWidget() {"
            'giveADayWidget.initialize("giveaday-widget", 2924, "organization", "large", "fr","#34B78F");}'
            "renderWidget();"
            "</script>"
        )


class IIdeluxWastePlugin(Interface):
    """"""


@implementer(IIdeluxWastePlugin)
class IdeluxWastePlugin(BasePlugin):
    def __call__(self, parts, config={}):
        # https://www.odwb.be/api/explore/v2.1/catalog/datasets/guide-de-tri1/records
        if "www.odwb.be" in parts.netloc and "guide-de-tri1" in parts.path:
            self.parts = parts
            self.config = config
            return self
        return None

    # url = config["url"]
    # return (f'<a href="{url}/view_idelux_waste?portal_item_id={portal_item_id}">{msg}</a>')
    @property
    def contents(self):
        headers = {"Accept": "application/json"}
        try:
            # ?limit=-1 to get all records from an odwb table.
            response = requests.get(
                f"{self.parts.geturl()}?limit=-1", headers=headers, timeout=5
            )
            self.config["extra_params"] = response.json()
            return self.config["extra_params"]

        except requests.exceptions.Timeout:
            logger.warning(f"Timeout raised for requests : {self.url}")
            return None


class IInbwContainersAffluencePlugin(Interface):
    """"""


@implementer(IInbwContainersAffluencePlugin)
class InbwContainersAffluencePlugin(BasePlugin):
    def __call__(self, parts, config={}):
        if "www.odwb.be" in parts.netloc and "affluence" in parts.path:
            self.parts = parts
            self.config = config
            return self
        return None

    @property
    def contents(self):
        headers = {"Accept": "application/json"}
        try:
            response = requests.get(
                f"{self.parts.geturl()}&limit=-1", headers=headers, timeout=5
            )
            self.config["extra_params"] = json.dumps(response.json())
            return self.config["extra_params"]
        except requests.exceptions.Timeout:
            logger.warning(f"Timeout raised for requests : {self.url}")
            return None


class IOdwbWidgetPlugin(Interface):
    """"""


@implementer(IOdwbWidgetPlugin)
class OdwbWidgetPlugin(BasePlugin):
    def __call__(self, parts, config={}):
        # https://static.opendatasoft.com/ods-widgets
        if "static.opendatasoft.com" in parts.netloc:
            self.is_odwb_widget_plugins = True
            self.parts = parts
            self.config = config
            return self

    @property
    def contents(self):
        return self.config["extra_params"]


class UnknowServicePlugin(BasePlugin):
    def __call__(self, parts, config={}):
        self.parts = parts
        self.config = config
        return self

    @property
    def contents(self):
        current_lang = self.config["current_lang"]
        msg = _("Unknow service")
        msg = translate(msg, target_language=current_lang)
        return f'<p class="unknow_service">{msg}</p>'


@implementer(IArcgisViewUtils)
class ArcgisView(BrowserView):
    _footer = None

    @property
    def get_portal_item_id(self):
        return self.request.portal_item_id


class IdeluxWasteView(BrowserView):

    def __init__(self, context, request):
        """ """


class InbwContainersAffluenceView(BrowserView):

    def __init__(self, context, request):
        """ """


class IOdwbWidgetLayer(IDefaultBrowserLayer):
    """ """


@implementer(IOdwbViewUtils, IOdwbWidgetLayer)
class OdwbWidgetView(BrowserView):

    def __init__(self, context, request):
        """ """
