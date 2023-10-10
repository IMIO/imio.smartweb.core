# -*- coding: utf-8 -*-

from plone.app.layout.viewlets.httpheaders import HeaderViewlet


class OgpTagsViewlet(HeaderViewlet):
    def update(self):
        super(OgpTagsViewlet, self).update()
