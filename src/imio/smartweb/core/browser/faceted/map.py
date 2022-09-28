# -*- coding: utf-8 -*-

from collective.faceted.map.browser.map import MapView
from imio.smartweb.core.browser.faceted.views import FolderView
from Products.Five import BrowserView


class FacetedMapView(FolderView, MapView):
    """Faceted map view"""


class FacetedGeoJSONPopup(BrowserView):
    def popup(self, brain):
        url = brain.getURL()
        title = brain.Title
        description = brain.Description
        if brain.has_leadimage:
            # TODO : beta1 : Get scale url from catalog
            img_url = f"{url}/@@images/image/mini"
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
