# -*- coding: utf-8 -*-

from imio.smartweb.core.config import DIRECTORY_URL
from imio.smartweb.core.contents.rest.base import BaseEndpoint
from imio.smartweb.core.contents.rest.base import BaseService
from imio.smartweb.core.utils import hash_md5
from plone import api
from plone.restapi.interfaces import IExpandableElement
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


class BaseDirectoryEndpoint(BaseEndpoint):
    def __call__(self):
        results = super(BaseDirectoryEndpoint, self).__call__()
        if not results.get("items"):
            return results
        orientation = self.context.orientation
        for result in results["items"]:
            modified_hash = hash_md5(result["modified"])
            if result.get("image"):
                self.convert_cached_image_scales(
                    result, modified_hash, orientation=orientation
                )
            if result.get("logo"):
                self.convert_cached_image_scales(
                    result, modified_hash, "logo", ["thumb"], ""
                )
            for sub_content in result.get("items", []):
                if sub_content["@type"] != "Image":
                    continue
                self.convert_cached_image_scales(
                    sub_content, modified_hash, "image", ["preview"], ""
                )
        return results

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
            "fullobjects=1",
            "sort_on=sortable_title",
            "b_size={}".format(self.context.nb_results),
        ]
        if self.context.selected_categories is not None:
            for category in self.context.selected_categories:
                params.append(f"taxonomy_contact_category.query={category}")
            params.append("taxonomy_contact_category.operator=or")
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


class DirectoryEndpointGet(BaseService):
    def reply(self):
        return DirectoryEndpoint(self.context, self.request)()


class DirectoryFiltersEndpointGet(BaseService):
    def reply(self):
        return DirectoryFiltersEndpoint(self.context, self.request)()
