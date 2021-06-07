# -*- coding: utf-8 -*-
from Products.CMFPlone.utils import base_hasattr
from Products.Five.browser import BrowserView

import re


class RichDescription(BrowserView):
    def description(self):
        """Description with html carriage return and bold"""
        description = ""
        if base_hasattr(self.context, "description"):
            description = self.context.description or ""
        # **strong**
        description = re.sub(r"\*\*([^\*\*]*)\*\*", r"<strong>\1</strong>", description)
        # *italic*
        description = re.sub(r"\*([^\*]*)\*", r"<em>\1</em>", description)
        # <br/>
        description = "<br/>".join(description.split("\r\n"))
        return description
