# -*- coding: utf-8 -*-

from imio.smartweb.core.interfaces import IViewWithoutLeadImage
from plone import api
from Products.Five import BrowserView
from zope.interface import implementer


@implementer(IViewWithoutLeadImage)
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

    @property
    def orientation(self):
        return self.context.orientation

    @property
    def current_language(self):
        return api.portal.get_current_language()[:2]
