# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.rest.view import BaseRestView
from imio.smartweb.core.interfaces import IOgpViewUtils
from plone import api
from zope.interface import implementer


@implementer(IOgpViewUtils)
class CampaignViewView(BaseRestView):
    """CampaignView view"""

    @property
    def propose_url(self):
        return self.context.propose_project_url

    @property
    def display_map(self):
        return self.context.display_map

    @property
    def local_query_zones_url(self):
        base_url = self.context.absolute_url()
        return f"{base_url}/@zones"

    @property
    def local_query_topics_url(self):
        base_url = self.context.absolute_url()
        return f"{base_url}/@all_topics"
