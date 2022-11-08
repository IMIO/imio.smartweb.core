# -*- coding: utf-8 -*-

from datetime import date
from imio.smartweb.core.config import EVENTS_URL
from imio.smartweb.core.contents.rest.base import BaseEndpoint
from imio.smartweb.core.contents.rest.base import BaseService
from plone.restapi.interfaces import IExpandableElement
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


class BaseEventsEndpoint(BaseEndpoint):
    @property
    def query_url(self):
        today = date.today().isoformat()
        params = [
            "selected_agendas={}".format(self.context.selected_agenda),
            "portal_type=imio.events.Event",
            "metadata_fields=category",
            "metadata_fields=topics",
            "metadata_fields=start",
            "metadata_fields=end",
            "metadata_fields=has_leadimage",
            "metadata_fields=UID",
            "event_dates.query={}".format(today),
            "event_dates.range=min",
            "sort_on=event_dates",
            "fullobjects=1",
            "b_size={}".format(self.context.nb_results),
        ]
        if self.context.selected_event_types is not None:
            for event_type in self.context.selected_event_types:
                params.append(f"event_type={event_type}")
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


class EventsEndpointGet(BaseService):
    def reply(self):
        return EventsEndpoint(self.context, self.request)()


class EventsFiltersEndpointGet(BaseService):
    def reply(self):
        return EventsFiltersEndpoint(self.context, self.request)()
