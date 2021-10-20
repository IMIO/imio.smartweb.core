# -*- coding: utf-8 -*-

from datetime import date
from imio.smartweb.core.config import EVENTS_URL
from imio.smartweb.core.contents.rest.base import BaseEndpoint
from plone.rest import Service
from plone.restapi.interfaces import IExpandableElement
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface

import json


class BaseEventsEndpoint(BaseEndpoint):
    @property
    def query_url(self):
        start = date.today().isoformat()
        params = [
            "selected_agendas={}".format(self.context.selected_agenda),
            "portal_type=imio.events.Event",
            "metadata_fields=category",
            "metadata_fields=topics",
            "metadata_fields=start",
            "metadata_fields=end",
            "metadata_fields=has_leadimage",
            "metadata_fields=UID",
            "start.query={}".format(start),
            "start.range=min",
            "sort_on=start",
            "sort_limit={}".format(self.context.nb_results),
        ]
        params = self.get_extra_params(params)
        url = f"{EVENTS_URL}/{self.remote_endpoint}?{'&'.join(params)}"
        return url


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class EventsEndpoint(BaseEventsEndpoint):
    remote_endpoint = "@search"


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class EventsFiltersEndpoint(BaseEventsEndpoint):
    remote_endpoint = "@search-filters"


class EventsEndpointGet(Service):
    def render(self):
        related_items = EventsEndpoint(self.context, self.request)
        return json.dumps(
            related_items(),
            indent=2,
            separators=(", ", ": "),
        )


class EventsFiltersEndpointGet(Service):
    def render(self):
        related_items = EventsFiltersEndpoint(self.context, self.request)
        return json.dumps(
            related_items(),
            indent=2,
            separators=(", ", ": "),
        )
