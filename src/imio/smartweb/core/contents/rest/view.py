# -*- coding: utf-8 -*-

from plone import api
from Products.Five import BrowserView


class BaseRestView(BrowserView):
    @property
    def batch_size(self):
        return self.context.nb_results

    @property
    def local_query_url(self):
        base_url = self.context.absolute_url()
        return f"{base_url}/@results"

    @property
    def local_filters_query_url(self):
        base_url = self.context.absolute_url()
        return f"{base_url}/@results-filters"

    def get_current_language(self):
        return api.portal.get_current_language()[:2]
