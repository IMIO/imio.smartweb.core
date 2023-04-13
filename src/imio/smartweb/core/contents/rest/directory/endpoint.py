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
        for result in results["items"]:
            if result.get("image"):
                modified_hash = hash_md5(result["modified"])
                preview_scale = (
                    f"{result['@id']}/@@images/image/preview?cache_key={modified_hash}"
                )
                extralarge_scale = f"{result['@id']}/@@images/image/extralarge?cache_key={modified_hash}"
                affiche_scale = (
                    f"{result['@id']}/@@images/image/affiche?cache_key={modified_hash}"
                )
                result["image_preview_scale"] = preview_scale
                result["image_extralarge_scale"] = extralarge_scale
                result["image_affiche_scale"] = affiche_scale
            if result.get("logo"):
                modified_hash = hash_md5(result["modified"])
                thumb_scale = (
                    f"{result['@id']}/@@images/logo/thumb?cache_key={modified_hash}"
                )
                result["logo_thumb_scale"] = thumb_scale
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
