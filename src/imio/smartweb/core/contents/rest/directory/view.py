# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.rest.view import BaseRestView
from plone import api


class DirectoryViewView(BaseRestView):
    """DirectoryView view"""

    @property
    def propose_url(self):
        return api.portal.get_registry_record("smartweb.propose_directory_url")
