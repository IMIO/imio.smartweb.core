# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from imio.smartweb.core.config import DIRECTORY_URL
from imio.smartweb.core.utils import get_scale_url
from imio.smartweb.core.interfaces import IHtmxViewUtils
from imio.smartweb.core.interfaces import IViewWithoutLeadImage
from imio.smartweb.core.utils import get_json
from imio.smartweb.locales import SmartwebMessageFactory as _
from Products.CMFPlone.resources import add_bundle_on_request
from plone import api
from plone.app.content.browser.contents.rearrange import OrderContentsBaseAction
from plone.app.content.utils import json_loads
from plone.app.contenttypes.browser.folder import FolderView
from plone.app.contenttypes.browser.full_view import FullViewItem as BaseFullViewItem
from plone.memoize.view import memoize
from Products.CMFPlone import utils
from Products.CMFPlone.browser.navigation import PhysicalNavigationBreadcrumbs
from zope.component import getMultiAdapter
from zope.interface import implementer

import itertools


@implementer(IViewWithoutLeadImage)
@implementer(IHtmxViewUtils)
class PagesView(FolderView):
    """Pages view"""

    b_size = 70

    def __call__(self):
        # get gallery sections and sections with gallery
        galleries_sections = self.context.listFolderContents(
            contentFilter={
                "portal_type": [
                    "imio.smartweb.SectionGallery",
                    "imio.smartweb.SectionContact",
                ]
            }
        )
        if len(galleries_sections) > 0:
            add_bundle_on_request(self.request, "spotlight")
        for index, gs in enumerate(galleries_sections):
            if (
                gs.portal_type == "imio.smartweb.SectionContact"
                and gs.gallery_mode != "gallery"
            ):
                galleries_sections.pop(index)
        if len(galleries_sections) > 0:
            add_bundle_on_request(self.request, "flexbin")
        return self.index()

    @memoize
    def get_page_contacts(self):
        # TODO We need to check every tests to be sure to avoid caching that
        # creates false positive assertions
        sections_contacts = self.context.listFolderContents(
            contentFilter={
                "portal_type": [
                    "imio.smartweb.SectionContact",
                ]
            }
        )
        if len(sections_contacts) == 0:
            return None
        nested_contact_list = [
            section_contacts.related_contacts
            for section_contacts in sections_contacts
            if section_contacts.related_contacts is not None
        ]
        if nested_contact_list == []:
            return None
        # Make a "set" to simplifying request in url (avoid duplicate uid)
        # Sometimes we have duplicate uid because some pages were build with contact attributes
        # in a section and for layout issues,for the same contact, others attributes are in another section.
        page_contacts = list(
            set(list(itertools.chain.from_iterable(nested_contact_list)))
        )
        uids = "&UID=".join(page_contacts)
        bsize = len(page_contacts)
        url = "{}/@search?UID={}&fullobjects=1&b_size={}".format(
            DIRECTORY_URL, uids, bsize
        )
        current_lang = api.portal.get_current_language()[:2]
        if current_lang != "fr":
            url = f"{url}&translated_in_{current_lang}=1"
        json_data = get_json(url)
        if json_data is None or len(json_data.get("items", [])) == 0:
            return
        return json_data

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

    @property
    def no_items_message(self):
        return _("There is no section on this page.")

    def get_class(self, obj):
        section_type = obj.portal_type.split(".")[-1]
        return " ".join(
            filter(
                None,
                [
                    section_type.lower(),
                    obj.css_class or "",
                    obj.bootstrap_css_class or "",
                    self.background_style(obj) and "with-background" or "",
                ],
            )
        )

    def background_style(self, obj):
        if not obj.background_image:
            return ""
        scale_url = get_scale_url(
            obj, self.request, "background_image", "affiche", "paysage"
        )
        css_bg_image = f"background-image:url({scale_url});"
        css_bg_size = "background-size:cover;"
        return " ".join([css_bg_image, css_bg_size])


class PagesFullViewItem(BaseFullViewItem):
    """Page view item"""

    def __init__(self, context, request):
        super(PagesFullViewItem, self).__init__(context, request)
        self.can_edit_sections = api.user.has_permission(
            "Modify portal content", obj=context
        )


class PagesFullViewItemWithoutEdit(BaseFullViewItem):
    """Page view item without sections edit tools"""

    can_edit_sections = False


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
