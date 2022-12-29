# -*- coding: utf-8 -*-

from datetime import date
from datetime import datetime
from datetime import timedelta
from imio.smartweb.core.config import EVENTS_URL
from imio.smartweb.core.contents.rest.base import BaseEndpoint
from imio.smartweb.core.contents.rest.base import BaseService
from plone.event.recurrence import recurrence_sequence_ical
from plone.event.utils import pydt
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.serializer.converters import json_compatible
from pytz import utc
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface

import copy
import dateutil


def expand_occurences(events):
    expanded_events = []

    for event in events:
        if not event["recurrence"]:
            expanded_events.append(event)
            continue
        start_date = dateutil.parser.parse(event["start"])
        start_date = start_date.astimezone(utc)
        end_date = dateutil.parser.parse(event["end"])
        end_date = end_date.astimezone(utc)

        start_dates = recurrence_sequence_ical(
            start=start_date,
            recrule=event["recurrence"],
            from_=datetime.now(),
        )

        if event["whole_day"] or event["open_end"]:
            duration = timedelta(hours=23, minutes=59, seconds=59)
        else:
            duration = end_date - start_date

        for occurence_start in start_dates:
            if pydt(start_date.replace(microsecond=0)) == occurence_start:
                expanded_events.append(event)
            else:
                new_event = copy.deepcopy(event)
                new_event["start"] = json_compatible(occurence_start)
                new_event["end"] = json_compatible(occurence_start + duration)
                expanded_events.append(new_event)

    return expanded_events


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

    def __call__(self):
        res = super(EventsEndpoint, self).__call__()
        if res == []:
            return res

        expanded_events = expand_occurences(res["items"])
        res["items"] = expanded_events
        res["items_total"] = len(expanded_events)

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
