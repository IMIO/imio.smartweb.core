# -*- coding: utf-8 -*-

from imio.smartweb.core.config import DIRECTORY_URL
from imio.smartweb.core.contents.rest.base import BaseEndpoint
from plone import api
from plone.rest import Service
from plone.restapi.interfaces import IExpandableElement
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface

import json


class BaseDirectoryEndpoint(BaseEndpoint):
    @property
    def query_url(self):
        entity_uid = api.portal.get_registry_record("smartweb.directory_entity_uid")
        params = [
            "selected_entities={}".format(entity_uid),
            "portal_type=imio.directory.Contact",
            "metadata_fields=facilities",
            "metadata_fields=taxonomy_contact_category",
            "metadata_fields=topics",
            "metadata_fields=has_leadimage",
            "sort_on=sortable_title",
        ]
        if self.context.selected_categories is not None:
            for category in self.context.selected_categories:
                params.append(f"taxonomy_contact_category={category}")
        params = self.get_extra_params(params)
        url = f"{DIRECTORY_URL}/{self.remote_endpoint}?{'&'.join(params)}"
        return url


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class DirectoryEndpoint(BaseDirectoryEndpoint):
    remote_endpoint = "@search"


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class DirectoryFiltersEndpoint(BaseDirectoryEndpoint):
    remote_endpoint = "@search-filters"


class DirectoryEndpointGet(Service):
    def render(self):
        response = self.request.response
        response.setHeader("Content-type", "application/json")
        related_items = DirectoryEndpoint(self.context, self.request)
        return json.dumps(
            related_items(),
            indent=2,
            separators=(", ", ": "),
        )


class DirectoryFiltersEndpointGet(Service):
    def render(self):
        response = self.request.response
        response.setHeader("Content-type", "application/json")
        related_items = DirectoryFiltersEndpoint(self.context, self.request)
        return json.dumps(
            related_items(),
            indent=2,
            separators=(", ", ": "),
        )
