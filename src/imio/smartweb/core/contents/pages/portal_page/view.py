# -*- coding: utf-8 -*-

from imio.smartweb.core.interfaces import IHtmxViewUtils
from Products.Five.browser import BrowserView
from zope.interface import implementer


@implementer(IHtmxViewUtils)
class NoTitleView(BrowserView):
    def __call__(self):
        return ""
