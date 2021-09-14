# -*- coding: utf-8 -*-

from Products.Five import BrowserView


class NewsViewView(BrowserView):
    """NewsView view"""

    @property
    def local_query_url(self):
        return "{}/@news".format(self.context.absolute_url())
