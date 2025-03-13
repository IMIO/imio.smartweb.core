# -*- coding: utf-8 -*-

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
        results = super(BaseEventsEndpoint, self).__call__() or {}
        if not results or not results.get("items"):
            return results
        orientation = self.context.orientation
        for result in results["items"]:
            modified_hash = hash_md5(result["modified"])
            if result.get("image"):
                self.convert_cached_image_scales(
                    result, modified_hash, orientation=orientation
                )
            for sub_content in result.get("items", []):
                if sub_content["@type"] != "Image":
                    continue
                self.convert_cached_image_scales(
                    sub_content, modified_hash, "image", ["preview"], ""
                )
        return results

    @property
    def query_url(self):
        params = [
            "selected_agendas={}".format(self.context.selected_agenda),
            "metadata_fields=category",
            "metadata_fields=local_category",
            "metadata_fields=container_uid",
            "metadata_fields=topics",
            "metadata_fields=start",
            "metadata_fields=end",
            "metadata_fields=has_leadimage",
            "metadata_fields=UID",
            "sort_on=event_dates",
            "fullobjects={}".format(self.fullobjects),
        ]
        if self.batch_size == 0:
            params.append("b_size={}".format(self.context.nb_results))
        else:
            params.append("b_size={}".format(self.batch_size))
        if self.context.selected_event_types is not None:
            for event_type in self.context.selected_event_types:
                params.append(f"event_type={event_type}")
        params = self.construct_query_string(params)
        url = f"{EVENTS_URL}/{self.remote_endpoint}?{params}"
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

    def reply_for_given_object(self, obj, request, fullobjects=1, batch_size=0):
        return EventsEndpoint(
            obj, request, fullobjects=fullobjects, batch_size=batch_size
        )()


class EventsFiltersEndpointGet(BaseService):
    def reply(self):
        return EventsFiltersEndpoint(self.context, self.request)()
