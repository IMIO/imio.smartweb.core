# -*- coding: utf-8 -*-

from imio.smartweb.core.behaviors.new_tab import INewTab
from imio.smartweb.core.contents.sections.views import CarouselOrTableSectionView
from imio.smartweb.core.utils import batch_results
from imio.smartweb.core.utils import get_scale_url
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from zope.i18n import translate


class LinksView(CarouselOrTableSectionView):
    """Links Section view"""

    def items(self):
        orientation = self.context.orientation
        image_scale = self.image_scale
        items = self.context.listFolderContents()
        results = []
        for item in items:
            url = item.absolute_url()
            is_anon = api.user.is_anonymous()
            if hasattr(item, "remoteUrl") and item.remoteUrl is not None and is_anon:
                portal_url = api.portal.get().absolute_url()
                url = item.remoteUrl.replace("${portal_url}", portal_url)
            has_icon = has_image = False
            if getattr(item.aq_base, "svg_icon", None):
                has_icon = True
            elif getattr(item.aq_base, "image", None):
                has_image = True
            scale_url = get_scale_url(
                item, self.request, "image", image_scale, orientation
            )

            results.append(
                {
                    "title": item.title,
                    "description": item.description,
                    "url": url,
                    "icon": item.svg_icon,
                    "has_icon": has_icon,
                    "image": scale_url,
                    "has_image": has_image,
                    "open_in_new_tab": INewTab(item).open_in_new_tab,
                }
            )
        return batch_results(results, self.context.nb_results_by_batch)

    def a_tag_item_title(self, item):
        title = item.get("title") or ""
        if item.get("open_in_new_tab", False):
            current_lang = api.portal.get_current_language()[:2]
            new_tab_txt = translate(_("New tab"), target_language=current_lang)
            return f"{title} ({new_tab_txt})"
        return title
