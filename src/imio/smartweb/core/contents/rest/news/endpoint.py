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

    @property
    def query_url(self):
        # Temporary use fullobjects=1 to get inner news contents
        # This should does the job !?
        # https://github.com/IMIO/imio.news.core/commit/fe63e9945c2880abdf2d74374e8bbc2e86b7b6a3#diff-6a114600617a2e65a563a363d1825914a8d9afe1608812eb0e2373b3cec93e1fR16
        params = [
            "selected_news_folders={}".format(self.context.selected_news_folder),
            "portal_type=imio.news.NewsItem",
            "metadata_fields=category",
            "metadata_fields=local_category",
            "metadata_fields=container_uid",
            "metadata_fields=topics",
            "metadata_fields=has_leadimage",
            "metadata_fields=UID",
            "sort_on=effective",
            "sort_order=descending",
            "fullobjects={}".format(self.fullobjects),
        ]
        if self.batch_size == 0:
            params.append("b_size={}".format(self.context.nb_results))
        else:
            params.append("b_size={}".format(self.batch_size))
        params = self.construct_query_string(params)
        url = f"{NEWS_URL}/{self.remote_endpoint}?{params}"
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

    def reply_for_given_object(self, obj, request, fullobjects=1, batch_size=0):
        return NewsEndpoint(
            obj, request, fullobjects=fullobjects, batch_size=batch_size
        )()


class NewsFiltersEndpointGet(BaseService):
    def reply(self):
        return NewsFiltersEndpoint(self.context, self.request)()
