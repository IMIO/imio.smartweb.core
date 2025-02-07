# -*- coding: utf-8 -*-
from imio.smartweb.core.contents import IPublication
from imio.smartweb.core.contents.sections.views import CarouselOrTableSectionView
from imio.smartweb.core.utils import batch_results
from imio.smartweb.core.utils import get_scale_url
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from zope.component import queryMultiAdapter
from zope.i18n import translate
from zope.interface import alsoProvides


class FilesView(CarouselOrTableSectionView):
    """Files Section view"""

    def items(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        orientation = self.context.orientation
        image_scale = self.image_scale
        items = super(FilesView, self).items()
        results = []
        for item in items:
            url = item.absolute_url()
            has_image = True if getattr(item.aq_base, "image", None) else False
            file_view = queryMultiAdapter((item, self.request), name="file_view")
            scale_url = get_scale_url(
                item, self.request, "image", image_scale, orientation
            )
            dict_item = {
                "title": item.title,
                "description": item.description,
                "smartweb_type": item.smartweb_type,
                "url": url,
                "image": scale_url,
                "has_image": has_image,
                "open_in_new_tab": True,
            }
            dict_item["item_infos"] = (
                None if file_view is None else file_view.human_readable_size()
            )
            if IPublication.providedBy(item):
                extra_properties = [
                    "linked_publication",
                    "publication_datetime",
                    "publication_url",
                    "publication_document_type",
                    "publication_attached_file",
                ]
                dict_item = self.get_publication_extra_properties(
                    item, dict_item, extra_properties
                )

            results.append(dict_item)
        return batch_results(results, self.context.nb_results_by_batch)

    def retrieve_item_url(self, item):
        if item.get("publication_url", None) is not None and api.user.is_anonymous():
            # return "real" publication url in iadeliberation
            return item.get("publication_url")
        # return smartweb item url
        return item.get("url")

    def get_publication_extra_properties(self, item, dict_item, extra_properties):
        for prop in extra_properties:
            dict_item[prop] = getattr(item, prop, None)
        return dict_item

    def a_tag_item_title(self, item):
        # Files always open in a new tab
        title = item.get("title") or ""
        current_lang = api.portal.get_current_language()[:2]
        new_tab_txt = translate(_("New tab"), target_language=current_lang)
        return f"{title} ({new_tab_txt})"
