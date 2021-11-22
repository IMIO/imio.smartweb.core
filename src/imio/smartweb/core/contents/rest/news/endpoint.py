# -*- coding: utf-8 -*-

from imio.smartweb.core.config import NEWS_URL
from imio.smartweb.core.contents.rest.base import BaseEndpoint
from plone.rest import Service
from plone.restapi.interfaces import IExpandableElement
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface

import json


class BaseNewsEndpoint(BaseEndpoint):
    @property
    def query_url(self):
        params = [
            "selected_news_folders={}".format(self.context.selected_news_folder),
            "portal_type=imio.news.NewsItem",
            "metadata_fields=category",
            "metadata_fields=topics",
            "metadata_fields=has_leadimage",
            "metadata_fields=UID",
            "sort_on=effective",
            "sort_order=descending",
            "sort_limit={}".format(self.context.nb_results),
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


class NewsEndpointGet(Service):
    def render(self):
        response = self.request.response
        response.setHeader("Content-type", "application/json")
        related_items = NewsEndpoint(self.context, self.request)
        return json.dumps(
            related_items(),
            indent=2,
            separators=(", ", ": "),
        )


class NewsFiltersEndpointGet(Service):
    def render(self):
        response = self.request.response
        response.setHeader("Content-type", "application/json")
        related_items = NewsFiltersEndpoint(self.context, self.request)
        return json.dumps(
            related_items(),
            indent=2,
            separators=(", ", ": "),
        )
