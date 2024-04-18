# -*- coding: utf-8 -*-

from plone import api
from plone.app.layout.viewlets.httpheaders import HeaderViewlet


class HtmxViewlet(HeaderViewlet):
    """htmx"""

    def update(self):
        super(HtmxViewlet, self).update()

    @property
    def is_anonymous(self):
        return api.user.is_anonymous()
