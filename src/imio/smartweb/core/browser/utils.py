# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from imio.smartweb.core.contents import IPages
from imio.smartweb.core.contents.pages.procedure.utils import sign_url
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from plone.api.portal import get_registry_record
from plone.formwidget.geolocation.vocabularies import _ as _geo
from zope.component import getMultiAdapter
from zope.i18n import translate

import json
import requests


class UtilsView(BrowserView):
    """ """

    def is_previewable_content(self):
        if not IPages.providedBy(self.context):
            return False

        context_state = getMultiAdapter(
            (self.context, self.request), name="plone_context_state"
        )
        return context_state.is_view_template()

    def has_gdpr_text(self):
        return api.portal.get_registry_record(
            "imio.gdpr.interfaces.IGDPRSettings.is_text_ready", default=False
        )

    def map_configuration(self):
        """Returns global map configuration from registry"""
        map_layers = get_registry_record("geolocation.map_layers") or []
        config = {
            "fullscreencontrol": get_registry_record("geolocation.fullscreen_control"),
            "locatecontrol": get_registry_record("geolocation.locate_control"),
            "zoomcontrol": get_registry_record("geolocation.zoom_control"),
            "minimap": get_registry_record("geolocation.show_minimap"),
            "addmarker": get_registry_record("geolocation.show_add_marker"),
            "geosearch": get_registry_record("geolocation.show_geosearch"),
            "geosearch_provider": get_registry_record("geolocation.geosearch_provider"),
            "default_map_layer": get_registry_record("geolocation.default_map_layer"),
            "map_layers": [
                {"title": translate(_geo(layer), context=self.request), "id": layer}
                for layer in map_layers
            ],
            "latitude": get_registry_record("geolocation.default_latitude"),
            "longitude": get_registry_record("geolocation.default_longitude"),
        }
        return json.dumps(config)

    def is_eguichet_aware(self):
        self.request.response.setHeader("Content-Type", "application/json")
        url = api.portal.get_registry_record("smartweb.url_formdefs_api")
        key = api.portal.get_registry_record("smartweb.secret_key_api")
        orig = "ia.smartweb"
        if not url:
            return json.dumps(
                {"value": False, "text": _("smartweb.settings : No url define")}
            )
        if not key:
            return json.dumps(
                {"value": False, "text": _("smartweb.settings : No secret key define")}
            )
        query_full = sign_url(url, key, orig)
        response = requests.get(query_full, timeout=10)
        return json.dumps(
            {
                "status_code": response.status_code,
                "value": True,
                "text": _(response.reason),
            }
        )
