# -*- coding: utf-8 -*-
from Products.Five import BrowserView

import logging

logger = logging.getLogger("Plone")


class ViewView(BrowserView):
    """ """

    @property
    def local_query_url(self):
        return "{}/@events".format(self.context.absolute_url())

    # @property
    # def get_events_portal_url(self):
    #     return "https://events.staging.imio.be/imio-events-entity/administration-communale-de-belleville/2021"
