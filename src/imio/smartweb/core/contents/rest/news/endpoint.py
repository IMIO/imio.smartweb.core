# -*- coding: utf-8 -*-

from imio.smartweb.core.config import NEWS_URL
from imio.smartweb.core.contents.rest.base import BaseEndpoint
from imio.smartweb.core.contents.rest.base import BaseService
from plone.restapi.interfaces import IExpandableElement
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


class BaseNewsEndpoint(BaseEndpoint):
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
