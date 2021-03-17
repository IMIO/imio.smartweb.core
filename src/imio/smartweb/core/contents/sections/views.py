# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from zope.interface import Interface


class ISectionView(Interface):
    """"""


class SectionView(BrowserView):
    """Section view"""

    def __call__(self):
        page = self.context.aq_parent
        url = "{}#{}".format(page.absolute_url(), self.context.id)
        return self.request.response.redirect(url)
