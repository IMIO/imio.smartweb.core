# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.rest.view import BaseRestView
from imio.smartweb.core.interfaces import IOgpViewUtils
from zope.interface import implementer


@implementer(IOgpViewUtils)
class CampaignViewView(BaseRestView):
    """CampaignView view"""

    @property
    def display_map(self):
        return self.context.display_map
