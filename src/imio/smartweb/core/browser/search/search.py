# -*- coding: utf-8 -*-

from plone import api
from Products.CMFPlone.browser.search import Search
from Products.CMFPlone.utils import normalizeString


class Search(Search):
    valid_keys = ("sort_on", "sort_order", "sort_limit", "fq", "fl", "facet", "core")

    def results(self):
        self._core = None
        self._query_parameters = {}
        return super(Search, self).results()

    def results_news(self):
        self._core = "news"
        self._query_parameters = {"portal_type": ["imio.news.NewsItem"]}
        return super(Search, self).results()

    def filter_query(self, query):
        query = super(Search, self).filter_query(query)
        if self._core is not None:
            query["core"] = self._core
        if self._query_parameters:
            query.update(self._query_parameters)
        return query

    def get_item_url(self, item):
        """Return a local url depending of current website config for remote items"""
        mapping = {
            "imio.news.NewsItem": "imio.smartweb.NewsView",
        }
        view_type = mapping.get(item.portal_type)
        if not view_type:
            # This should never happen
            raise NotImplementedError
        content_view = api.content.find(context=api.portal.get(), portal_type=view_type)
        if not content_view:
            # This mean that there is no content listing
            raise ValueError("Missing content type {0}".format(view_type))
        # XXX Use informations from content view and item to determinate the right
        # context
        item_id = normalizeString(item.Title)
        return "{container}/{id}?u={uid}".format(
            container=content_view[0].getURL(),
            id=item_id,
            uid=item.UID,
        )
