# -*- coding: utf-8 -*-

from Products.CMFPlone.resources import add_bundle_on_request
from plone.app.content.browser.contents.rearrange import OrderContentsBaseAction
from plone.app.content.utils import json_loads
from plone.app.contenttypes.browser.folder import FolderView
from plone.app.contenttypes.browser.full_view import FullViewItem as BaseFullViewItem
from zope.interface import Interface
from zope.interface import implementer


class IPagesView(Interface):
    """Marker interface for Pages Views"""


@implementer(IPagesView)
class PagesView(FolderView):
    """Pages view"""

    def __call__(self):
        galleries_sections = self.context.listFolderContents(
            contentFilter={"portal_type": "imio.smartweb.SectionGallery"}
        )
        if len(galleries_sections) > 0:
            add_bundle_on_request(self.request, "spotlightjs")
            add_bundle_on_request(self.request, "flexbin")
        return self.index()

    def get_class(self, obj):
        section_type = obj.portal_type.split(".")[-1]
        return "{} {}".format(section_type.lower(), obj.css_class)


class PagesFullViewItem(BaseFullViewItem):
    """Page view item"""


class PagesOrderingView(OrderContentsBaseAction):
    """Page sections ordering view"""

    def __call__(self):
        self.protect()
        form = self.request.form
        id = form.get("id")
        delta = int(form.get("delta"))
        ordering = self.getOrdering()
        ordered_ids = json_loads(form.get("orderedSectionsIds", "null"))
        if ordered_ids:
            position_id = [(ordering.getObjectPosition(i), i) for i in ordered_ids]
            position_id.sort()
            if ordered_ids != [i for position, i in position_id]:
                return
        ordering.moveObjectsByDelta([id], delta, ordered_ids)
