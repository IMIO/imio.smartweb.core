# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.rest.base import BaseEndpoint
from imio.smartweb.core.contents.rest.base import BaseService
from imio.smartweb.core.utils import get_basic_auth_json
from plone import api
from plone.restapi.interfaces import IExpandableElement
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class CampaignEndpoint(BaseEndpoint):

    def __call__(self):
        user = api.portal.get_registry_record("smartweb.iaideabox_api_username")
        pwd = api.portal.get_registry_record("smartweb.iaideabox_api_password")
        results = get_basic_auth_json(self.query_url, user, pwd)
        if not results:
            return {}
        elif "data" in results:
            return results.get("data")
        else:
            return results

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
            url = f"{combo_api_url}/cards/imio-ideabox-projet/list?campagne={campaign_id}&full=on"
        return url


class CampaignEndpointGet(BaseService):
    def reply(self):
        return CampaignEndpoint(self.context, self.request)()
