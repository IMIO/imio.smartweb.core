# -*- coding: utf-8 -*-

from imio.smartweb.core.config import DIRECTORY_URL
from imio.smartweb.core.config import EVENTS_URL
from imio.smartweb.core.config import NEWS_URL
from imio.smartweb.core.contents.rest.search.endpoint import get_default_view_url
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

import requests


@implementer(IPublishTraverse)
class BaseRequestForwarder(Service):
    def __init__(self, context, request):
        super().__init__(context, request)
        self.traversal_stack = []

    def reply(self):
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
        headers = {"Accept": "application/json"}
        params = self.request.form
        data = json_body(self.request)

        # Forward the request to the authentic source
        auth_source_response = requests.request(
            method, url, params=params, headers=headers, data=data
        )

        response = self.request.response
        # Set the status code and headers from the authentic source server response
        response.setStatus(auth_source_response.status_code)
        for header, value in auth_source_response.headers.items():
            response.setHeader(header, value)

        return auth_source_response.json()

    def add_smartweb_urls(self, json_data):
        for item in json_data.get("items", []):
            if "@id" in item and "UID" in item:
                # we can construct a Smartweb-related URL for item
                # TODO: handle other views & translations (use/refactor code in
                # search endpoint)
                # TODO 2: always get UID and ID to construct URL ?
                default_view_url = get_default_view_url(self.request_type)
                item_uid = item["UID"]
                item["smartweb_url"] = f"{default_view_url}/#content?u={item_uid}"
        return json_data


class DirectoryRequestForwarder(BaseRequestForwarder):
    request_type = "directory"
    base_url = DIRECTORY_URL


class EventsRequestForwarder(BaseRequestForwarder):
    request_type = "events"
    base_url = EVENTS_URL


class NewsRequestForwarder(BaseRequestForwarder):
    request_type = "news"
    base_url = NEWS_URL
