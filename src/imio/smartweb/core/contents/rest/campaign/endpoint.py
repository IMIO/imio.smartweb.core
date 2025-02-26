# -*- coding: utf-8 -*-

from imio.smartweb.common.utils import get_vocabulary
from imio.smartweb.core.contents.rest.base import BaseEndpoint
from imio.smartweb.core.contents.rest.base import BaseService
from imio.smartweb.core.utils import get_basic_auth_json
from imio.smartweb.core.utils import get_ts_api_url
from plone import api
from plone.restapi.interfaces import IExpandableElement
from zope.component import adapter
from zope.i18n import translate
from zope.interface import implementer
from zope.interface import Interface

import base64
import requests


def get_ideabox_basic_auth_header() -> str:
    user = api.portal.get_registry_record("smartweb.iaideabox_api_username")
    pwd = api.portal.get_registry_record("smartweb.iaideabox_api_password")
    usrPass = f"{user}:{pwd}".encode("utf-8")
    b64Val = base64.b64encode(usrPass)
    return f"Basic {b64Val.decode('utf-8')}"


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class CampaignEndpoint(BaseEndpoint):

    def __call__(self):
        require_keys = [
            "uuid",
            "id",
            "display_name",
            "text",
            "url",
            "api_url",
            "fields",
            "workflow",
        ]
        user = api.portal.get_registry_record("smartweb.iaideabox_api_username")
        pwd = api.portal.get_registry_record("smartweb.iaideabox_api_password")
        json = get_basic_auth_json(self.query_url, user, pwd)
        json_res = {}
        if not json:
            return {}
        elif "data" in json:
            # list of projects
            json["data"] = self.add_b64_image_to_data(json.get("data"))
            projects = [
                {k: v for k, v in d.items() if k in require_keys}
                for d in json.get("data")
            ]
            json_res["items"] = projects
            json_res["items_total"] = json.get("count")

        else:
            # single project
            json.pop("evolution")
            json.pop("roles")
            json.pop("submission")
            json.pop("user")
            json_res = json
        # Return a json which represents a project or which contains a list of projects
        return json_res

    def add_b64_image_to_data(self, data):
        for d in data:
            # get image
            image_url = d.get("fields").get("images_raw")[0].get("image").get("url")
            content = self.get_image(image_url).content
            b64_content = base64.b64encode(content).decode("utf-8")
            d["fields"]["images_raw"][0]["image"]["content"] = b64_content
        return data

    def get_image(self, image_url):
        if not image_url:
            return
        headers = {"Accept": "image/*"}
        headers["Authorization"] = get_ideabox_basic_auth_header()
        response = requests.get(image_url, headers=headers)
        return response

    @property
    def query_url(self):
        wcs_api = get_ts_api_url("wcs")
        if "id" in self.request.form:
            # we want a specific project
            project_id = self.request.form.get("id")
            url = f"{wcs_api}/cards/imio-ideabox-projet/{project_id}?full=on"
        else:
            # we want list of projects for a specific campaign with eventually extra pamams (zone, topic, ...)
            extra_params = [f"{k}={v}" for k, v in self.request.form.items()]
            extra_params = "&".join(extra_params)
            campaign_id = self.context.linked_campaign
            url = f"{wcs_api}/cards/imio-ideabox-projet/list?campagne={campaign_id}&full=on&filter-statut=Vote|Enregistr%C3%A9e&filter-statut-operator=in&{extra_params}"
        return url


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class ZonesEndpoint(BaseEndpoint):

    def __call__(self):
        json_res = {}
        user = api.portal.get_registry_record("smartweb.iaideabox_api_username")
        pwd = api.portal.get_registry_record("smartweb.iaideabox_api_password")
        json = get_basic_auth_json(self.query_url, user, pwd)
        json_res["items"] = json["data"]
        json_res["items_total"] = json.get("count")
        return json_res

    @property
    def query_url(self):
        wcs_api = get_ts_api_url("wcs")
        campaign_id = self.context.linked_campaign
        url = f"{wcs_api}/cards/imio-ideabox-zone/list?campagne={campaign_id}&full=on"
        return url


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class TopicsEndpoint(BaseEndpoint):

    def __call__(self):
        topics_vocabulary = get_vocabulary("imio.smartweb.vocabulary.Topics")
        current_lang = api.portal.get_current_language()[:2]
        json_res = {
            "items": [
                {
                    "value": term.value,
                    "title": translate(term.title, target_language=current_lang),
                }
                for term in topics_vocabulary
            ],
            "items_total": len(topics_vocabulary),
        }
        return json_res


class CampaignEndpointGet(BaseService):
    def reply(self):
        return CampaignEndpoint(self.context, self.request)()


class AuthCampaignEndpointGet(BaseService):
    def reply(self):
        return get_ideabox_basic_auth_header()


class ZonesEndpointGet(BaseService):
    def reply(self):
        return ZonesEndpoint(self.context, self.request)()


class TopicsEndpointGet(BaseService):
    def reply(self):
        return TopicsEndpoint(self.context, self.request)()
