# -*- coding: utf-8 -*-

from plone.app.layout.viewlets.httpheaders import HeaderViewlet


class HtmxViewlet(HeaderViewlet):
    """htmx"""

    def update(self):
        super(HtmxViewlet, self).update()
