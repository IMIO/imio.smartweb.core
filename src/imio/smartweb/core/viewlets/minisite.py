# -*- coding: utf-8 -*-

from imio.smartweb.core.behaviors.minisite import IImioSmartwebMinisite
from plone import api
from plone.app.layout.viewlets import common
from urllib.parse import urlparse


class MinisitePortalLinkViewlet(common.ViewletBase):
    """ """

    def get_hostname(self):
        portal_url = api.portal.get().absolute_url()
        domain = urlparse(portal_url).netloc
        if domain.startswith("www."):
            domain = domain[4:]
        return domain

    def available(self):
        root = api.portal.get_navigation_root(self.context)
        return IImioSmartwebMinisite.providedBy(root)
