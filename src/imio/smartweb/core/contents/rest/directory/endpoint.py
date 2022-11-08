# -*- coding: utf-8 -*-

from imio.smartweb.core.config import DIRECTORY_URL
from imio.smartweb.core.contents.rest.base import BaseEndpoint
from imio.smartweb.core.contents.rest.base import BaseService
from plone import api
from plone.restapi.interfaces import IExpandableElement
from zope.component import adapter
from zope.component import getUtility
from zope.interface import implementer
from zope.interface import Interface
from zope.schema.interfaces import IVocabularyFactory


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
            "fullobjects=1",
            "sort_on=sortable_title",
            "b_size={}".format(self.context.nb_results),
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

    def __call__(self):
        res = super(DirectoryEndpoint, self).__call__()
        if res == []:
            return res
        filtered_items = []
        # Selected category (in faceted view)
        selected_contact_category_token = self.request.form.get(
            "taxonomy_contact_category"
        )
        if selected_contact_category_token is None:
            return res

        factory = getUtility(
            IVocabularyFactory, "imio.smartweb.vocabulary.DirectoryCategories"
        )
        vocabulary = factory(api.portal.get())
        selected_contact_category_title = vocabulary.getTerm(
            selected_contact_category_token
        ).title

        for item in res.get("items"):
            for tcc in item.get("taxonomy_contact_category"):
                if tcc.get("title").startswith(selected_contact_category_title):
                    filtered_items.append(item)
                    break

        res["items"] = filtered_items
        res["items_total"] = len(filtered_items)
        return res


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class DirectoryFiltersEndpoint(BaseDirectoryEndpoint):
    remote_endpoint = "@search-filters"

    def __call__(self):
        res = super(DirectoryFiltersEndpoint, self).__call__()
        if res == []:
            return res
        filtered_categories_title = []

        if self.context.selected_categories is None:
            return res

        for selected_category_token in self.context.selected_categories:
            for category in res.get("taxonomy_contact_category"):
                if category.get("token") == selected_category_token:
                    filtered_categories_title.append(category.get("title"))

        filtered_categories = []
        for title in filtered_categories_title:
            for category in res.get("taxonomy_contact_category"):
                if title in category.get("title"):
                    filtered_categories.append(category)
        res["taxonomy_contact_category"] = filtered_categories
        return res


class DirectoryEndpointGet(BaseService):
    def reply(self):
        return DirectoryEndpoint(self.context, self.request)()


class DirectoryFiltersEndpointGet(BaseService):
    def reply(self):
        return DirectoryFiltersEndpoint(self.context, self.request)()
