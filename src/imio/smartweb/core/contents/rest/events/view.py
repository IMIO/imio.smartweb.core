# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.rest.view import BaseRestView
from plone import api


class EventsViewView(BaseRestView):
    """EventsView view"""

    @property
    def propose_url(self):
        return api.portal.get_registry_record("smartweb.propose_events_url")
