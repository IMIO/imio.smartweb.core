# -*- coding: utf-8 -*-


from imio.smartweb.core.utils import get_json
from plone import api
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.search.handler import SearchHandler
from plone.restapi.search.utils import unflatten_dotted_dict
from plone.restapi.services import Service
from Products.CMFCore.utils import getToolByName
from zExceptions import Unauthorized
from zope.component import getMultiAdapter

import logging

logger = logging.getLogger("imio.events.core")


class FindEndpointHandler(SearchHandler):
    def search(self, query=None):
        results = {"items": []}
        portal = api.portal.get()
        get_types_url = f"{portal.absolute_url()}/@types"
        auth_header = self.request._orig_env.get("HTTP_AUTHORIZATION", None)
        types = get_json(get_types_url, auth=auth_header, timeout=20)
        if not types:
            raise Unauthorized("No types found, you are not allowed to search")
        self._constrain_query_by_path(query)
        query = self._parse_query(query)
        if query.get("type_of_request") == "count_contents_types":
            results = self.count_contents_types(query)
        elif query.get("type_of_request") == "find_big_files_or_images":
            results = self.find_big_files_or_images(query)
        elif query.get("type_of_request") == "get_max_depth":
            results = self.get_max_depth()
        else:
            return super().search(query)
        return results

    def count_contents_types(self, query):
        results = {"items": []}
        if query.get("operator") == "and":
            query["path"]["depth"] = -1
            lazy_resultset = self.catalog.searchResults(**query)
            results = {
                "items": [
                    {
                        "portal_type": query.get("portal_type"),
                        "nb_items": len(lazy_resultset),
                    }
                ]
            }
        else:
            portal_types = (
                query.get("portal_type")
                if isinstance(query.get("portal_type"), list)
                else [query.get("portal_type")] if query.get("portal_type") else []
            )
            for portal_type in portal_types:
                new_query = query.copy()
                new_query["portal_type"] = portal_type
                lazy_resultset = self.catalog.searchResults(**new_query)
                results["items"].append(
                    {"portal_type": portal_type, "nb_items": len(lazy_resultset)}
                )
        # fullobjects = False
        # results = getMultiAdapter((lazy_resultset, self.request), ISerializeToJson)(
        #     fullobjects=fullobjects
        # )
        return results

    def find_big_files_or_images(self, query):
        SIZE_LIMIT = query.get("size", "1000000")
        results = {"items": []}
        lazy_resultset = self.catalog.searchResults(**query)
        for brain in lazy_resultset:
            obj = brain.getObject()
            blob = getattr(obj, "file", None) or getattr(obj, "image", None)
            if blob and hasattr(blob, "getSize"):
                size = blob.getSize()
                if size > int(SIZE_LIMIT):
                    results["items"].append(
                        {
                            "title": obj.title,
                            "portal_type": obj.portal_type,
                            "url": obj.absolute_url(),
                            "size": round(size / (1024 * 1024), 2),
                        }
                    )
        return results

    def get_max_depth(self):
        portal = api.portal.get()
        catalog = getToolByName(portal, "portal_catalog")

        max_depth = 0
        results = {"items": []}

        for brain in catalog():
            path = brain.getPath()
            depth = len(path.strip("/").split("/"))
            if depth > max_depth:
                max_depth = depth
                results["items"] = [{"path": path, "depth": depth}]
            elif depth == max_depth:
                results["items"].append({"path": path, "depth": depth})
        results["max_depth"] = max_depth
        return results


class FindEndpoint(Service):
    def reply(self):
        query = self.request.form.copy()
        query = unflatten_dotted_dict(query)
        return FindEndpointHandler(self.context, self.request).search(query)
