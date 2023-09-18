# -*- coding: utf-8 -*-

from imio.smartweb.core.utils import hash_md5
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from plone.locking.browser.info import LockInfoViewlet
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five.browser import BrowserView
from zope.annotation.interfaces import IAnnotations
from zope.interface import alsoProvides
from zope.interface import Interface
from zope.lifecycleevent import modified

import json


SECTION_ITEMS_HASH_KEY = "sections-items-hash-key"


class ISectionView(Interface):
    """ """


class SectionView(BrowserView):
    """Section view"""

    def __call__(self):
        self.redirect_to_section(self.context.id)

    def locking_info(self):
        return LockInfoViewlet(self.context, self.request, None, None).render()

    def redirect_to_section(self, section_id):
        page = self.context.aq_parent
        url = "{}#section-{}".format(page.absolute_url(), section_id)
        self.request.response.redirect(url)

    def hide_section_title(self):
        if not self.context.can_toggle_title_visibility:
            return
        if self.context.collapsible_section:
            return
        self.context.hide_title = True
        api.portal.show_message(_("Section title has been hidden"), self.request)
        self.redirect_to_section(self.context.id)

    def show_section_title(self):
        if not self.context.can_toggle_title_visibility:
            return
        self.context.hide_title = False
        api.portal.show_message(_("Section title has been shown"), self.request)
        self.redirect_to_section(self.context.id)

    @property
    def is_anonymous(self):
        return api.user.is_anonymous()


class CarouselOrTableSectionView(SectionView):
    """Section view that can display a carousel"""

    @property
    def image_scale(self):
        layout = self.context.getLayout()
        # scales used depend on the batch size
        if layout == "carousel_view":
            return self.context.nb_results_by_batch == 1 and "affiche" or "vignette"
        elif layout == "table_view":
            return self.context.nb_results_by_batch == 1 and "liste" or "vignette"
        else:
            return getattr(self.context, "image_scale", "")


class HashableJsonSectionView(SectionView):
    json_data = None

    def refresh_modification_date(self):
        new_hash = None
        if self.json_data is not None:
            new_hash = hash_md5(json.dumps(self.json_data))
        annotations = IAnnotations(self.context)
        stored_hash = annotations.get(SECTION_ITEMS_HASH_KEY)
        if stored_hash != new_hash:
            alsoProvides(self.request, IDisableCSRFProtection)
            modified(self.context)
            annotations[SECTION_ITEMS_HASH_KEY] = new_hash
