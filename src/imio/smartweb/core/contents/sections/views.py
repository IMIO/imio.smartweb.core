# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from zope.interface import Interface


class ISectionView(Interface):
    """"""


class SectionView(BrowserView):
    """Section view"""

    def __call__(self):
        page = self.context.aq_parent
        return self.request.response.redirect(page.absolute_url())
