# -*- coding: utf-8 -*-

from imio.smartweb.core.config import DIRECTORY_URL
from imio.smartweb.core.config import EVENTS_URL
from imio.smartweb.core.config import NEWS_URL
from imio.smartweb.core.contents.rest.search.endpoint import get_default_view_url
from imio.smartweb.core.utils import get_wca_token
from plone.protect.interfaces import IDisableCSRFProtection
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

import os
import requests


@implementer(IPublishTraverse)
class BaseRequestForwarder(Service):
    def __init__(self, context, request):
        super().__init__(context, request)
        self.traversal_stack = []

    def reply(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        url = "/".join(self.traversal_stack)
        auth_source_url = f"{self.base_url}/{url}"
        response = self.forward_request(auth_source_url)
        response = self.add_smartweb_urls(response)
        return response

    def publishTraverse(self, request, name):
        self.traversal_stack.append(name)
        return self

    def forward_request(self, url):
        method = self.request.method
        token = get_wca_token(self.client_id, self.client_secret)
        headers = {"Accept": "application/json", "Authorization": token}
        params = self.request.form
        if method == "GET":
            params = self.add_missing_metadatas(params)
        data = json_body(self.request)

        # Forward the request to the authentic source
        auth_source_response = requests.request(
            method, url, params=params, headers=headers, json=data
        )
        response = self.request.response
        # Set the status code and headers from the authentic source server response
        response.setStatus(auth_source_response.status_code)
        for header, value in auth_source_response.headers.items():
            response.setHeader(header, value)

        if auth_source_response.status_code == 204 or auth_source_response.text == "":
            # Empty response
            return ""

        return auth_source_response.json()

    def construct_url(self, view_url, item):
        # we can construct a Smartweb-related URL for item
        # TODO: handle other views & translations (use/refactor code in
        # search endpoint)
        item_uid = item["UID"]
        item_id = item.get("id", "content")
        item["smartweb_url"] = f"{view_url}/{item_id}?u={item_uid}"

    def add_smartweb_urls(self, json_data):
        if "items" not in json_data and "@id" not in json_data:
            return json_data
        default_view_url = get_default_view_url(self.request_type)
        if "@id" in json_data and "UID" in json_data:
            self.construct_url(default_view_url, json_data)
            return json_data
        for item in json_data.get("items", []):
            if "@id" in item and "UID" in item:
                self.construct_url(default_view_url, item)
        return json_data

    def add_missing_metadatas(self, params):
        if "fullobjects" in params:
            return params
        if "metadata_fields" not in params:
            params["metadata_fields"] = ["id", "UID"]
        else:
            if "id" not in params["metadata_fields"]:
                params["metadata_fields"].append("id")
            if "UID" not in params["metadata_fields"]:
                params["metadata_fields"].append("UID")
        return params


class DirectoryRequestForwarder(BaseRequestForwarder):
    request_type = "directory"
    client_id = os.environ.get("RESTAPI_DIRECTORY_CLIENT_ID")
    client_secret = os.environ.get("RESTAPI_DIRECTORY_CLIENT_SECRET")
    base_url = DIRECTORY_URL


class EventsRequestForwarder(BaseRequestForwarder):
    request_type = "events"
    client_id = os.environ.get("RESTAPI_EVENTS_CLIENT_ID")
    client_secret = os.environ.get("RESTAPI_EVENTS_CLIENT_SECRET")
    base_url = EVENTS_URL


class NewsRequestForwarder(BaseRequestForwarder):
    request_type = "news"
    client_id = os.environ.get("RESTAPI_NEWS_CLIENT_ID")
    client_secret = os.environ.get("RESTAPI_NEWS_CLIENT_SECRET")
    base_url = NEWS_URL
