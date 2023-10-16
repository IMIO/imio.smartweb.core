# -*- coding: utf-8 -*-

from imio.smartweb.core.contents import IRestView
from ZPublisher.BaseRequest import DefaultPublishTraverse
from zope.component import adapts
from zope.publisher.interfaces.http import IHTTPRequest


class RestViewTraversable(DefaultPublishTraverse):
    """ """

    adapts(IRestView, IHTTPRequest)

    def publishTraverse(self, request, name):
        if "u" in self.request.form and name != "view":
            return self.context

        return super(RestViewTraversable, self).publishTraverse(request, name)
