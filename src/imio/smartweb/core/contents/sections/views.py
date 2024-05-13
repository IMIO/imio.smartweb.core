# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from imio.smartweb.common.utils import get_vocabulary
from imio.smartweb.common.utils import translate_vocabulary_term
from imio.smartweb.core.utils import hash_md5
from imio.smartweb.core.utils import reindexParent
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from plone.locking.browser.info import LockInfoViewlet
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five.browser import BrowserView
from zope.annotation.interfaces import IAnnotations
from zope.i18n import translate
from zope.interface import alsoProvides
from zope.interface import Interface
from zope.lifecycleevent import modified

import json
import pytz


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
    def display_container_title(self):
        return False

    @property
    def is_anonymous(self):
        return api.user.is_anonymous()

    def get_section_size(self):
        current_lang = api.portal.get_current_language()[:2]
        if not self.context.bootstrap_css_class:
            return translate(_("Define section size"), target_language=current_lang)
        return translate_vocabulary_term(
            "imio.smartweb.vocabulary.BootstrapCSS",
            self.context.bootstrap_css_class,
            current_lang,
        )

    @property
    def get_sizes(self):
        voc = get_vocabulary("imio.smartweb.vocabulary.BootstrapCSS")
        sizes = [{"key": t.token, "value": _(t.title)} for t in voc]
        return sizes

    @property
    def save_size(self):
        select_name = f"select_{self.context.UID()}"
        if not self.request.form.get(select_name):
            return json.dumps({})
        section_size = self.request.form.get(select_name)
        context = aq_inner(self.context)
        context.bootstrap_css_class = section_size
        context.reindexObject()
        reindexParent(context)
        current_lang = api.portal.get_current_language()[:2]
        size_txt = translate_vocabulary_term(
            "imio.smartweb.vocabulary.BootstrapCSS",
            section_size,
            current_lang,
        )
        return json.dumps({"id": section_size, "title": size_txt})


class CarouselOrTableSectionView(SectionView):
    """Section view that can display a carousel"""

    @property
    def image_scale(self):
        layout = self.context.getLayout()
        # scales used depend on the batch size
        if layout == "carousel_view":
            return self.context.nb_results_by_batch == 1 and "affiche" or "vignette"
        elif layout == "table_view":
            return self.context.nb_results_by_batch == 1 and "affiche" or "vignette"
        else:
            return getattr(self.context, "image_scale", "")

    def datetime_format(self, item):
        """
        item.get("effective", None)
        => DateTime('YYYY/MM/DD HH:mm:ss.000000 GMT+1')
        convert to more conventional datetime format
        and return its string representation
        """
        effective = item.get("effective", None)
        if effective is None:
            return ""
        target_timezone = pytz.timezone("Europe/Paris")
        if isinstance(effective, str):
            return effective
        dt = effective.asdatetime()
        target_datetime = dt.astimezone(target_timezone)
        output_format = "%Y-%m-%dT%H:%M:%S%z"
        formatted_datetime_str = target_datetime.strftime(output_format)
        return formatted_datetime_str


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
