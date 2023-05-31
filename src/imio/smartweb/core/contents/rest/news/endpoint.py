# -*- coding: utf-8 -*-

from imio.smartweb.core.config import NEWS_URL
from imio.smartweb.core.contents.rest.base import BaseEndpoint
from imio.smartweb.core.contents.rest.base import BaseService
from imio.smartweb.core.utils import hash_md5
from plone.restapi.interfaces import IExpandableElement
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


class BaseNewsEndpoint(BaseEndpoint):
    def __call__(self):
        results = super(BaseNewsEndpoint, self).__call__()
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
            res = result.get("items")
            if res is None:
                continue
            for item in res:
                if item.get("image"):
                    modified_hash = hash_md5(result["modified"])
                    preview_item_scale = f"{item['@id']}/@@images/image/preview?cache_key={modified_hash}"
                    extralarge_item_scale = f"{item['@id']}/@@images/image/extralarge?cache_key={modified_hash}"
                    affiche_item_scale = f"{item['@id']}/@@images/image/affiche?cache_key={modified_hash}"
                    item["image_preview_scale"] = preview_item_scale
                    item["image_extralarge_scale"] = extralarge_item_scale
                    item["image_affiche_scale"] = affiche_item_scale
        return results

    @property
    def query_url(self):
        # Temporary use fullobjects=1 to get inner news contents
        # This should does the job !?
        # https://github.com/IMIO/imio.news.core/commit/fe63e9945c2880abdf2d74374e8bbc2e86b7b6a3#diff-6a114600617a2e65a563a363d1825914a8d9afe1608812eb0e2373b3cec93e1fR16
        params = [
            "selected_news_folders={}".format(self.context.selected_news_folder),
            "portal_type=imio.news.NewsItem",
            "metadata_fields=category",
            "metadata_fields=topics",
            "metadata_fields=has_leadimage",
            "metadata_fields=UID",
            "sort_on=effective",
            "sort_order=descending",
            "b_size={}".format(self.context.nb_results),
            "fullobjects=1",
        ]
        params = self.get_extra_params(params)
        url = f"{NEWS_URL}/{self.remote_endpoint}?{'&'.join(params)}"
        return url


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class NewsEndpoint(BaseNewsEndpoint):
    remote_endpoint = "@search"


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class NewsFiltersEndpoint(BaseNewsEndpoint):
    remote_endpoint = "@search-filters"


class NewsEndpointGet(BaseService):
    def reply(self):
        return NewsEndpoint(self.context, self.request)()


class NewsFiltersEndpointGet(BaseService):
    def reply(self):
        return NewsFiltersEndpoint(self.context, self.request)()
