# -*- coding: utf-8 -*-

from datetime import date
from imio.smartweb.core.config import EVENTS_URL
from imio.smartweb.core.contents.rest.base import BaseEndpoint
from imio.smartweb.core.contents.rest.base import BaseService
from imio.smartweb.core.utils import hash_md5
from plone.restapi.interfaces import IExpandableElement
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


class BaseEventsEndpoint(BaseEndpoint):
    def __call__(self):
        results = super(BaseEventsEndpoint, self).__call__()
        # https://agenda.enwallonie.be/braine-lalleud/citoyens/bc573e7592ee4f6498ad3cba8097358e/@@images/image/preview?
        if not results.get("items"):
            return results
        for result in results["items"]:
            if result.get("image"):
                modified_hash = hash_md5(result["modified"])
                preview_scale = (
                    f"{result['@id']}/@@images/image/preview?cache_key={modified_hash}"
                )
                extralarge_scale = f"{result['@id']}/@@images/image/extralarge?cache_key={modified_hash}"
                affiche_scale = (
                    f"{result['@id']}/@@images/image/affiche?cache_key={modified_hash}"
                )
                result["image_preview_scale"] = preview_scale
                result["image_extralarge_scale"] = extralarge_scale
                result["image_affiche_scale"] = affiche_scale
        return results

    @property
    def query_url(self):
        today = date.today().isoformat()
        params = [
            "selected_agendas={}".format(self.context.selected_agenda),
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
    remote_endpoint = "@events"


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
