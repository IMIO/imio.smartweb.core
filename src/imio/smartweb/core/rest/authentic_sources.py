# -*- coding: utf-8 -*-

from imio.smartweb.core.config import DIRECTORY_URL
from imio.smartweb.core.config import EVENTS_URL
from imio.smartweb.core.config import NEWS_URL
from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

import requests


class BaseRequestForwarder(BrowserView):
    def __call__(self):
        traversal_stack = getattr(self, "traversal_stack", [])
        url = "/".join(traversal_stack)
        auth_source_url = f"{self.base_url}/{url}"
        return self.forward_request(auth_source_url)

    @implementer(IPublishTraverse)
    def publishTraverse(self, request, name):
        if not hasattr(self, "traversal_stack"):
            self.traversal_stack = []
        self.traversal_stack.append(name)
        return self

    def browserDefault(self, request):
        return self, ()

    def forward_request(self, url):
        method = self.request.method
        headers = {"Accept": self.request.environ["HTTP_ACCEPT"]}
        params = self.request.form

        data = {}
        if self.request.get("BODY") is not None:
            data = self.request.get("BODY")

        # Forward the request to the authentic source
        auth_source_response = requests.request(
            method, url, params=params, headers=headers, data=data
        )

        response = self.request.response
        # Set the status code and headers from the authentic source server response
        response.setStatus(auth_source_response.status_code)
        for header, value in auth_source_response.headers.items():
            response.setHeader(header, value)

        return auth_source_response.text


class DirectoryRequestForwarder(BaseRequestForwarder):
    base_url = DIRECTORY_URL


class EventsRequestForwarder(BaseRequestForwarder):
    base_url = EVENTS_URL


class NewsRequestForwarder(BaseRequestForwarder):
    base_url = NEWS_URL
