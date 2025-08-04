# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import common
from plone.app.layout.viewlets.httpheaders import HeaderViewlet
from zope.component import queryMultiAdapter
from zope.viewlet.interfaces import IViewletManager


class PortalHeaderTopContainerViewlet(common.ViewletBase):
    """Viewlet containing the top header viewlets manager"""


class IPortalHeaderTopContainerViewletManager(IViewletManager):
    """Viewlet manager containing top header viewlets"""


class NoIndexedViewlet(HeaderViewlet):
    """Pages that should not be indexed by search engines"""

    def render(self):
        request = self.request
        b_start = int(request.get("b_start", 0))
        b_size = int(request.get("b_size", 10))
        total = self.view.total if hasattr(self.view, "total") else 0

        base_url = self.context.absolute_url()
        links = []

        if b_start > 0:
            prev_start = max(0, b_start - b_size)
            links.append(
                f'<link rel="prev" total="{total}" href="{base_url}/index_html?b_start={prev_start}&amp;b_size={b_size}" />'
            )

        if (b_start + b_size) < total:
            next_start = b_start + b_size
            links.append(
                f'<link rel="next" total="{total}" href="{base_url}/index_html?b_start={next_start}&amp;b_size={b_size}" />'
            )

        return "\n".join(links)

    def update(self):
        super(NoIndexedViewlet, self).update()
        # This page should not be indexed, we set the X-Robots-Tag header
        self.request.response.setHeader("X-Robots-Tag", "noindex, follow")
