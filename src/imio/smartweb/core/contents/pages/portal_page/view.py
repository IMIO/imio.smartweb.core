# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView


class NoTitleView(BrowserView):
    def __call__(self):
        return ""
