# -*- coding: utf-8 -*-
from Products.CMFPlone.utils import base_hasattr
from Products.Five.browser import BrowserView


class RichDescription(BrowserView):
    def description(self):
        """Description with html carriage return"""
        description = ""
        if base_hasattr(self.context, "description"):
            description = self.context.description or ""

        description = "<br/>".join(description.split("\r\n"))
        return description
