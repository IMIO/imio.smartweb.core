# -*- coding: utf-8 -*-

from imio.smartweb.common.utils import is_log_active
from imio.smartweb.core.config import DIRECTORY_URL
from imio.smartweb.core.config import EVENTS_URL
from imio.smartweb.core.config import NEWS_URL
from imio.smartweb.core.contents.rest.search.endpoint import get_default_view_url
from plone import api
from plone.i18n.normalizer import idnormalizer
from plone.protect.interfaces import IDisableCSRFProtection
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

import logging
import os
import requests

logger = logging.getLogger("imio.smartweb.core")


@implementer(IPublishTraverse)
class BaseRequestForwarder(Service):
    def __init__(self, context, request):
        super().__init__(context, request)
        self.traversal_stack = []

    def reply(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        url = "/".join(self.traversal_stack)
        if self.request_type == "events":
            url = url.replace("@search", "@events")
        auth_source_url = f"{self.base_url}/{url}"
        response = self.forward_request(auth_source_url)
        if isinstance(response, dict):
            response = self.enrich_response(response)
        if is_log_active():
            logger.info("======== FULL Response =========")
            logger.info(response)
        return response

    def enrich_response(self, response):
        uid = response.get("UID")
        if not uid:
            return response
        lang = api.portal.get_current_language(context=self.context)
        title = response.get(f"title_{lang}") or response.get("title")
        if title:
            slug = idnormalizer.normalize(title, locale=lang)
        else:
            slug = response.get("id", "content")
        view_url = get_default_view_url(self.request_type)
        response["smartweb_url"] = f"{view_url}/{slug}?u={uid}"
        return response

    def publishTraverse(self, request, name):
        self.traversal_stack.append(name)
        return self

    def forward_request(self, url):
        hop_by_hop = (
            "connection",
            "keep-alive",
            "proxy-authenticate",
            "proxy-authorization",
            "te",
            "trailer",
            "transfer-encoding",
            "upgrade",
        )
        method = self.request.method
        if method == "GET" and self.request.form.get("wcatoken") == "false":
            headers = {"Accept": "application/json"}
        else:
            auth_header = getattr(self.request, "_auth", "")
            headers = {"Accept": "application/json"}
            if auth_header and auth_header.startswith("Bearer "):
                headers["Authorization"] = auth_header
        self.request.form.pop("wcatoken", None)
        if is_log_active():
            logger.info("======== Forwarding request to AUTHENTIC SOURCE =========")
            logger.info(f"url to forward : {url} ({method})")
            for key, value in self.request.form.items():
                logger.info(f"param : {key} = {value}")
            logger.info(f"headers : {headers}")
        params = self.request.form
        if method == "GET":
            params = self.add_missing_metadatas(params)
        data = json_body(self.request)

        # Forward the request to the authentic source
        try:
            auth_source_response = requests.request(
                method, url, params=params, headers=headers, json=data, timeout=30
            )
        except requests.exceptions.RequestException as e:
            logger.error(f"Authentic source unreachable at {url}: {e}")
            self.request.response.setStatus(503)
            return ""
        response = self.request.response
        # Set the status code and headers from the authentic source server response
        response.setStatus(auth_source_response.status_code)
        for header, value in auth_source_response.headers.items():
            # Skip hop-by-hop headers
            # And also skip content-encoding because we forward uncompressed data
            if (
                header.lower() not in hop_by_hop
                and header.lower() != "content-encoding"
            ):
                response.setHeader(header, value)
        if auth_source_response.status_code == 204 or auth_source_response.text == "":
            # Empty response
            return ""
        if is_log_active():
            logger.info("======== Status code & header from AUTHENTIC SOURCE =========")
            logger.info(f"status code : {auth_source_response.status_code}")
            for key, value in auth_source_response.headers.items():
                logger.info(f"header : {key} = {value}")
        try:
            return auth_source_response.json()
        except ValueError:
            logger.error(
                f"Non-JSON response from authentic source {url} "
                f"(status {auth_source_response.status_code}): "
                f"{auth_source_response.text[:200]}"
            )
            self.request.response.setStatus(502)
            return ""

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

    def enrich_response(self, response):
        return super(DirectoryRequestForwarder, self).enrich_response(response)


class EventsRequestForwarder(BaseRequestForwarder):
    request_type = "events"
    client_id = os.environ.get("RESTAPI_EVENTS_CLIENT_ID")
    client_secret = os.environ.get("RESTAPI_EVENTS_CLIENT_SECRET")
    base_url = EVENTS_URL

    def enrich_response(self, response):
        return super(EventsRequestForwarder, self).enrich_response(response)


class NewsRequestForwarder(BaseRequestForwarder):
    request_type = "news"
    client_id = os.environ.get("RESTAPI_NEWS_CLIENT_ID")
    client_secret = os.environ.get("RESTAPI_NEWS_CLIENT_SECRET")
    base_url = NEWS_URL

    def enrich_response(self, response):
        return super(NewsRequestForwarder, self).enrich_response(response)
