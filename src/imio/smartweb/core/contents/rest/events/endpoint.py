# -*- coding: utf-8 -*-

from imio.smartweb.core.config import EVENTS_URL
from plone.rest import Service
from plone.restapi.interfaces import IExpandableElement
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface

import json
import requests


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class EventsEndpoint(object):

    language = "fr"

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        results = self.getResult()
        return results

    def getResult(self):
        headers = {"Accept": "application/json"}
        result = requests.get(self.query_url, headers=headers)
        return result.json()

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
