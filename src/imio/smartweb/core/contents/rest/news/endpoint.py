# -*- coding: utf-8 -*-

from imio.smartweb.core.config import NEWS_URL
from imio.smartweb.core.contents.rest.base import BaseEndpoint
from imio.smartweb.core.contents.rest.base import BaseService
from imio.smartweb.core.utils import get_json
from imio.smartweb.core.utils import hash_md5
from plone import api
from plone.restapi.interfaces import IExpandableElement
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


class BaseNewsEndpoint(BaseEndpoint):
    def __call__(self):
        results = super(BaseNewsEndpoint, self).__call__() or {}
        if not results.get("items"):
            return results
        orientation = self.context.orientation
        for result in results["items"]:
            modified_hash = hash_md5(result["modified"])
            if result.get("image"):
                self.convert_cached_image_scales(
                    result, modified_hash, orientation=orientation
                )
            for sub_content in result.get("items", []):
                if sub_content["@type"] != "Image":
                    continue
                self.convert_cached_image_scales(
                    sub_content, modified_hash, "image", ["preview"], ""
                )
        return results

    def _get_news_folders_uids_and_title_from_entity(self, entity_uid):
        url = f"{NEWS_URL}/@search_entity?UID={entity_uid}&metadata_fields=UID"

        data = get_json(url)
        entity_uid = data.get("items")[0].get("UID")
        url_to_get_news_folders = (
            f"{data.get('items')[0].get('@id')}"
            f"/@search_newsfolder_for_entity?portal_type=imio.news.NewsFolder&metadata_fields=UID&entity_uid={entity_uid}"
        )
        data = get_json(url_to_get_news_folders)
        uids = [item["UID"] for item in data["items"]]
        data = {item["UID"]: item["title"] for item in data["items"]}
        return uids, data

    @property
    def query_url(self):
        # Temporary use fullobjects=1 to get inner news contents
        # This should does the job !?
        # https://github.com/IMIO/imio.news.core/commit/fe63e9945c2880abdf2d74374e8bbc2e86b7b6a3#diff-6a114600617a2e65a563a363d1825914a8d9afe1608812eb0e2373b3cec93e1fR16
        entity_uid = api.portal.get_registry_record("smartweb.news_entity_uid")
        # Fallback if news folder is breaked (removed from auth source)
        uids, data = self._get_news_folders_uids_and_title_from_entity(entity_uid)
        selected_item = self.context.selected_news_folder
        if selected_item not in uids:
            item = next(
                (k for k, v in data.items() if "administration" in v.lower()),
                uids[0] if uids else None,
            )
            selected_item = item if item else None
            if not selected_item:
                selected_item = uids[0]
        params = [
            "selected_news_folders={}".format(selected_item),
            "portal_type=imio.news.NewsItem",
            "metadata_fields=category",
            "metadata_fields=local_category",
            "metadata_fields=container_uid",
            "metadata_fields=topics",
            "metadata_fields=has_leadimage",
            "metadata_fields=UID",
            "sort_on=effective",
            "sort_order=descending",
            "entity_uid={}".format(entity_uid),
            "fullobjects={}".format(self.fullobjects),
        ]
        self.request.form.update()
        updated_query_form = self.request.form
        if updated_query_form.get("batch_size", None):
            batch_size = updated_query_form.get("batch_size")
            params.append("b_size={}".format(batch_size))
        elif self.batch_size == 0:
            params.append("b_size={}".format(self.context.nb_results))
        else:
            params.append("b_size={}".format(self.batch_size))
        params = self.construct_query_string(params)
        url = f"{NEWS_URL}/{self.remote_endpoint}?{params}"
        return url


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class NewsEndpoint(BaseNewsEndpoint):
    remote_endpoint = "@search_newsitems"


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class NewsFiltersEndpoint(BaseNewsEndpoint):
    remote_endpoint = "@search-filters"


class NewsEndpointGet(BaseService):
    def reply(self):
        return NewsEndpoint(self.context, self.request)()

    def reply_for_given_object(self, obj, request, fullobjects=1, batch_size=0):
        return NewsEndpoint(
            obj, request, fullobjects=fullobjects, batch_size=batch_size
        )()


class NewsFiltersEndpointGet(BaseService):
    def reply(self):
        return NewsFiltersEndpoint(self.context, self.request)()
