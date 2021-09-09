# -*- coding: utf-8 -*-
from plone.registry.interfaces import IRegistry
from Products.Five import BrowserView
from zope.component import getUtility

import logging

logger = logging.getLogger("Plone")


class ViewView(BrowserView):
    """ """

    @property
    def local_query_url(self):
        return "{}/@news".format(self.context.absolute_url())
