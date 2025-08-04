# -*- coding: utf-8 -*-
from datetime import date
from imio.smartweb.core.browser.sitemap import format_sitemap_items
from imio.smartweb.core.browser.sitemap import get_endpoint_data
from imio.smartweb.core.contents import IDirectoryView
from imio.smartweb.core.contents import IEventsView
from imio.smartweb.core.contents import INewsView
from imio.smartweb.core.interfaces import INoIndexedUtils
from imio.smartweb.core.interfaces import IViewWithoutLeadImage
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from Products.Five import BrowserView
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
    def label(self):
        label = ""
        if IDirectoryView.providedBy(self.context):
            label = _("Contacts links")
        elif IEventsView.providedBy(self.context):
            label = _("Events links")
        elif INewsView.providedBy(self.context):
            label = _("News links")
        return label

    @property
    def get_data(self):
        return getattr(self, "items", [])

    @property
    def total(self):
        """Total number of items in the current view."""
        return getattr(self, "_total", 0)
