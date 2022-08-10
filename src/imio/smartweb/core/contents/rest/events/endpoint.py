# -*- coding: utf-8 -*-

from imio.smartweb.core.config import EVENTS_URL
from imio.smartweb.core.contents.rest.base import BaseEndpoint
from imio.smartweb.core.contents.rest.base import BaseService
from plone.restapi.interfaces import IExpandableElement
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface

import datetime


class BaseEventsEndpoint(BaseEndpoint):
    @property
    def query_url(self):
        today = datetime.date.today()
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
            "sort_limit={}".format(self.context.nb_results),
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

    def __call__(self):
        res = super(EventsEndpoint, self).__call__()
        if res == []:
            return res
        today = datetime.date.today()
        results = []
        for item in res.get("items"):
            if not item.get("end") or len(item.get("end")) == 0:
                pass
            else:
                enddate = datetime.datetime.strptime(
                    item.get("end"), "%Y-%m-%dT%H:%M:%S+00:00"
                ).date()
                # Filter : Don't get past events
                if enddate < today:
                    continue
            results.append(item)
        res["items"] = results
        res["items_total"] = len(results)
        return res


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
