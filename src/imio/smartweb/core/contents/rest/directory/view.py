# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.rest.view import BaseRestView
from imio.smartweb.core.interfaces import IOgpViewUtils
from plone import api
from zope.interface import implementer


@implementer(IOgpViewUtils)
class DirectoryViewView(BaseRestView):
    """DirectoryView view"""

    @property
    def propose_url(self):
        return api.portal.get_registry_record("smartweb.propose_directory_url")

    @property
    def display_map(self):
        return self.context.display_map
