# -*- coding: utf-8 -*-
from datetime import date
from imio.smartweb.core.browser.sitemap import format_sitemap_items
from imio.smartweb.core.browser.sitemap import get_endpoint_data
from imio.smartweb.core.config import DIRECTORY_URL
from imio.smartweb.core.config import EVENTS_URL
from imio.smartweb.core.config import NEWS_URL
from imio.smartweb.core.contents import IDirectoryView
from imio.smartweb.core.contents import IEventsView
from imio.smartweb.core.contents import INewsView
from imio.smartweb.core.interfaces import INoIndexedUtils
from imio.smartweb.core.interfaces import IViewWithoutLeadImage
from imio.smartweb.core.utils import get_json
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from Products.Five import BrowserView
from urllib.parse import parse_qs
from urllib.parse import urlsplit
from zope.interface import implementer


@implementer(IViewWithoutLeadImage)
class BaseRestView(BrowserView):
    @property
    def batch_size(self):
        return self.context.nb_results

    @property
    def local_query_url(self):
        base_url = self.context.absolute_url()
        return f"{base_url}/@results"

    @property
    def local_filters_query_url(self):
        base_url = self.context.absolute_url()
        return f"{base_url}/@results-filters"

    @property
    def orientation(self):
        return self.context.orientation

    @property
    def current_language(self):
        return api.portal.get_current_language()[:2]

    @property
    def context_authenticated_user(self):
        return api.user.is_anonymous()

    @property
    def view_path(self):
        url = self.context.absolute_url()
        parsed = urlsplit(url)
        return url.replace(f"{parsed.scheme}://{parsed.netloc}", "")

    @property
    def direct_access(self):
        query_string = self.request.get("QUERY_STRING", "")
        params = parse_qs(query_string)
        uuid = params.get("u", [None])[0]
        if uuid and self.request.HTTP_REFERER == "":
            endpoint = "@search"
            if IEventsView.providedBy(self.context):
                endpoint = "@events"
                url = EVENTS_URL
            if IDirectoryView.providedBy(self.context):
                url = DIRECTORY_URL
            if INewsView.providedBy(self.context):
                url = NEWS_URL
            url = f"{url}/{endpoint}?UID={uuid}&fullobjects=0"
            self._item = get_json(url)
            return True
        return False

    @property
    def item(self):
        item = self._item.get("items", [])[0] if self._item else None
        return item

    def _format_address(
        self, street=None, number=None, zipcode=None, city=None, country=None
    ):
        street_part = ", ".join(filter(None, [street, number]))
        city_part = " ".join(filter(None, [str(zipcode) if zipcode else None, city]))
        address_parts = [street_part, city_part]
        address = " - ".join(filter(None, address_parts))
        if country:
            address += f" / {country}"
        return address


@implementer(INoIndexedUtils)
class SeoHiddenReactLinks(BrowserView):

    DEFAULT_BATCH_SIZE = 100
    _total = 0

    def __call__(self):
        b_start = int(self.request.form.get("b_start", 0))
        b_size = int(self.request.form.get("b_size", self.DEFAULT_BATCH_SIZE))

        if IEventsView.providedBy(self.context):
            today = date.today().isoformat()
            self.request.form["event_dates.range"] = "min"
            self.request.form["event_dates.query"] = today

        # Inject batching params
        self.request.form["b_start"] = b_start
        self.request.form["b_size"] = b_size

        data = get_endpoint_data(self.context, self.request)
        self.items = format_sitemap_items(
            data.get("items", []), self.context.absolute_url()
        )

        self._total = data.get("items_total", len(self.items))
        self.b_start = b_start
        self.b_size = b_size
        return self.index()

    @property
    def default_view(self):
        return self.context.absolute_url()

    @property
    def label(self):
        label = ""
        if IDirectoryView.providedBy(self.context):
            label = _("Direcotry : SEO links")
        elif IEventsView.providedBy(self.context):
            label = _("Agenda : SEO links")
        elif INewsView.providedBy(self.context):
            label = _("News : SEO links")
        return label

    @property
    def get_data(self):
        return getattr(self, "items", [])

    @property
    def total(self):
        """Total number of items in the current view."""
        return getattr(self, "_total", 0)
