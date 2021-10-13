# -*- coding: utf-8 -*-

from imio.smartweb.core.config import EVENTS_URL
from imio.smartweb.core.contents.rest.base import BaseEndpoint
from plone.rest import Service
from plone.restapi.interfaces import IExpandableElement
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface

import json


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class EventsEndpoint(BaseEndpoint):
    @property
    def local_query_url(self):
        return "{}/@events".format(self.context.absolute_url())

    @property
    def query_url(self):
        params = [
            "selected_agendas={}".format(self.context.selected_agenda),
            "portal_type=imio.events.Event",
            "metadata_fields=category",
            "metadata_fields=start",
            "metadata_fields=end",
            "limit={}".format(self.context.nb_results),
        ]
        params = self.get_extra_params(params)
        url = "{}/@search?{}".format(EVENTS_URL, "&".join(params))
        return url


class EventsEndpointGet(Service):
    def render(self):
        related_items = EventsEndpoint(self.context, self.request)
        return json.dumps(
            related_items(),
            indent=2,
            sort_keys=True,
            separators=(", ", ": "),
        )
