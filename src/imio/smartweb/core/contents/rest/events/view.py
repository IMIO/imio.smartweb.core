# -*- coding: utf-8 -*-

from Products.Five import BrowserView


class EventsViewView(BrowserView):
    """EventsView view"""

    @property
    def local_query_url(self):
        return "{}/@events".format(self.context.absolute_url())
