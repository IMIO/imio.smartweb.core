# -*- coding: utf-8 -*-

from plone.app.layout.viewlets.httpheaders import HTTPCachingHeaders


class MyHTTPCachingHeaders(HTTPCachingHeaders):
    def update(self):
        super(MyHTTPCachingHeaders, self).update()

    def getHeaders(self):
        result = super(MyHTTPCachingHeaders, self).getHeaders()
        result.append(("prefix", "og: http://ogp.me/ns#"))
        return result
