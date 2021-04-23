# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from Products.CMFPlone.resources import add_bundle_on_request
from plone import api
from plone.app.content.browser.contents.rearrange import OrderContentsBaseAction
from plone.app.content.utils import json_loads
from plone.app.contenttypes.browser.folder import FolderView
from plone.app.contenttypes.browser.full_view import FullViewItem as BaseFullViewItem
from Products.CMFPlone import utils
from Products.CMFPlone.browser.navigation import PhysicalNavigationBreadcrumbs
from zope.component import getMultiAdapter
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

    def results(self, **kwargs):
        """
        Gets results for folder listings without taking care of friendly_types
        """
        # Extra filter
        kwargs.update(self.request.get("contentFilter", {}))
        kwargs.setdefault("batch", True)
        kwargs.setdefault("b_size", self.b_size)
        kwargs.setdefault("b_start", self.b_start)
        kwargs.setdefault("orphan", 1)

        listing = aq_inner(self.context).restrictedTraverse("@@folderListing", None)
        results = listing(**kwargs)
        return results

    def get_class(self, obj):
        section_type = obj.portal_type.split(".")[-1]
        return " ".join(
            [section_type.lower(), obj.css_class or "", obj.bootstrap_css_class or ""]
        )


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


class DefaultPagesBreadcrumbs(PhysicalNavigationBreadcrumbs):
    def breadcrumbs(self):
        """
        Change breadcrumbs behaviour for default pages :
            - anonymous user does not see the page
            - connected user sees the page
        """
        if not api.user.is_anonymous():
            return super(DefaultPagesBreadcrumbs, self).breadcrumbs()
        context = aq_inner(self.context)
        request = self.request
        container = utils.parent(context)
        view = getMultiAdapter((container, request), name="breadcrumbs_view")
        return tuple(view.breadcrumbs())
