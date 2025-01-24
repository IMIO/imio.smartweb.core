# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.rest.base import BaseEndpoint
from imio.smartweb.core.contents.rest.base import BaseService
from imio.smartweb.core.utils import get_basic_auth_json
from plone import api
from plone.restapi.interfaces import IExpandableElement
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface

import base64
import requests


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
        results = {}
        if not json:
            return {}
        elif "data" in json:
            # list of projects
            json["data"] = self.add_b64_image_to_data(json.get("data"))
            projet = [
                {k: v for k, v in d.items() if k in require_keys}
                for d in json.get("data")
            ]
            results["items"] = projet
            results["items_total"] = json.get("count")

        else:
            # single project
            results = json.get("data")
        return results

    def add_b64_image_to_data(self, data):
        for d in data:
            # get image
            image_url = d.get("fields").get("images_raw")[0].get("image").get("url")
            content = self.get_image(image_url).content
            b64_content = base64.b64encode(content).decode("utf-8")
            d["fields"]["images_raw"][0]["image"]["b64"] = b64_content
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
        combo_api_url = api.portal.get_registry_record("smartweb.url_combo_api")
        if "id" in self.request.form:
            # we want a specific project
            project_id = self.request.form.get("id")
            url = f"{combo_api_url}/cards/imio-ideabox-projet/{project_id}?full=on"
        else:
            # we want list of projects for a specific campaign
            campaign_id = self.context.linked_campaign
            url = f"{combo_api_url}/cards/imio-ideabox-projet/list?campagne={campaign_id}&full=on&filter-statut=Vote|Enregistr%C3%A9e&filter-statut-operator=in"
        return url


class CampaignEndpointGet(BaseService):
    def reply(self):
        return CampaignEndpoint(self.context, self.request)()


class AuthCampaignEndpointGet(BaseService):
    def reply(self):
        return get_ideabox_basic_auth_header()


def get_ideabox_basic_auth_header() -> str:
    user = api.portal.get_registry_record("smartweb.iaideabox_api_username")
    pwd = api.portal.get_registry_record("smartweb.iaideabox_api_password")
    usrPass = f"{user}:{pwd}".encode("utf-8")
    b64Val = base64.b64encode(usrPass)
    return f"Basic {b64Val.decode('utf-8')}"
