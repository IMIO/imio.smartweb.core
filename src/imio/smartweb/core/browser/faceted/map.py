# -*- coding: utf-8 -*-

from collective.faceted.map.browser.map import MapView
from imio.smartweb.core.utils import get_scale_url
from imio.smartweb.core.browser.faceted.views import FolderView
from Products.Five import BrowserView


class FacetedMapView(FolderView, MapView):
    """Faceted map view"""

    def get_scale_url(self, item):
        request = self.request
        orientation = self.context.orientation
        return get_scale_url(item, request, "image", "vignette", orientation)


class FacetedGeoJSONPopup(BrowserView):
    def popup(self, brain):
        url = brain.getURL()
        title = brain.Title
        description = brain.Description
        orientation = self.context.orientation
        if brain.has_leadimage:
            img_url = get_scale_url(brain, self.request, "image", "liste", orientation)
            return f"""<a href="{url}" title="{title}">
                         <img src="{img_url}" alt="{title}" />
                         <div>
                           <span class="popup_title">{title}</span>
                           <span class="popup_description">{description}</span>
                         </div>
                       </a>"""
        else:
            return f"""<a href="{url}" title="{title}">
                         <div>
                           <span class="popup_title">{title}</span>
                           <span class="popup_description">{description}</span>
                         </div>
                       </a>"""
