# -*- coding: utf-8 -*-

from Products.Five import BrowserView


class DirectoryViewView(BrowserView):
    """DirectoryView view"""

    @property
    def local_query_url(self):
        return "{}/@directory".format(self.context.absolute_url())
