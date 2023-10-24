# -*- coding: utf-8 -*-

from plone.app.layout.viewlets.httpheaders import HeaderViewlet


class ArcgisHeaderViewlet(HeaderViewlet):
    def update(self):
        super(ArcgisHeaderViewlet, self).update()

    # def getHeaders(self):
    #     import pdb;pdb.set_trace()
    #     result = super(ArcgisHeaderViewlet, self).getHeaders()
    #     result.append(("prefix", "og: http://ogp.me/ns#"))
    #     return result
