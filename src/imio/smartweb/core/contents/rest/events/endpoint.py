# -*- coding: utf-8 -*-
from imio.smartweb.core.config import EVENTS_URL
from imio.smartweb.core.utils import get_json
from plone import api
from plone.registry.interfaces import IRegistry
from plone.rest import Service
from plone.restapi.interfaces import IExpandableElement
from zope.component import adapter
from zope.component import getUtility
from zope.interface import implementer
from zope.interface import Interface

import json
import logging
import requests

logger = logging.getLogger("Plone")


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
        """
        SAMPLE : http://localhost:8080/Plone/@search
        ?selected_agendas=a84f2773e1c440bb947614148ccfd53f
        &selected_agendas=8787866afaa14379ab2e556b8d2e646c
        &metadata_fields=category
        &metadata_fields=start
        &metadata_fields=end
        """
        agenda_query = "selected_agendas={}".format(self.context.selected_agenda)
        url = "{}/@search?{}&metadata_fields=category&metadata_fields=start&metadata_fields=end".format(
            EVENTS_URL, agenda_query
        )
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
