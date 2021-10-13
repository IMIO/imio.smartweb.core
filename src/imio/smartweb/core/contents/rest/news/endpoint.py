# -*- coding: utf-8 -*-

from imio.smartweb.core.config import NEWS_URL
from imio.smartweb.core.contents.rest.base import BaseEndpoint
from plone.rest import Service
from plone.restapi.interfaces import IExpandableElement
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface

import json


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class NewsEndpoint(BaseEndpoint):
    @property
    def local_query_url(self):
        return "{}/@news".format(self.context.absolute_url())

    @property
    def query_url(self):
        params = [
            "selected_news_folders={}".format(self.context.selected_news_folder),
            "portal_type=imio.news.NewsItem",
            "metadata_fields=category",
            "limit={}".format(self.context.nb_results),
        ]
        params = self.get_extra_params(params)
        url = "{}/@search?{}".format(NEWS_URL, "&".join(params))
        return url


class NewsEndpointGet(Service):
    def render(self):
        related_items = NewsEndpoint(self.context, self.request)
        return json.dumps(
            related_items(),
            indent=2,
            sort_keys=True,
            separators=(", ", ": "),
        )
