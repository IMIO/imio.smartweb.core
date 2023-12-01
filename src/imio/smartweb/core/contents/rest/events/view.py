# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.rest.view import BaseRestView
from imio.smartweb.core.interfaces import IOgpViewUtils
from plone import api
from zope.interface import implementer


@implementer(IOgpViewUtils)
class EventsViewView(BaseRestView):
    """EventsView view"""

    @property
    def propose_url(self):
        return api.portal.get_registry_record("smartweb.propose_events_url")

    @property
    def display_map(self):
        return self.context.display_map
