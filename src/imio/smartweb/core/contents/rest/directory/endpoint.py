# -*- coding: utf-8 -*-

from imio.smartweb.core.config import DIRECTORY_URL
from imio.smartweb.core.contents.rest.base import BaseEndpoint
from plone.rest import Service
from plone.restapi.interfaces import IExpandableElement
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface

import json


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class DirectoryEndpoint(BaseEndpoint):
    @property
    def local_query_url(self):
        return "{}/@directory".format(self.context.absolute_url())

    @property
    def query_url(self):
        # ex : {'taxonomy_contact_category': '("token")', 'topics': 'education'}
        params = [
            "selected_entities={}".format(self.context.selected_entity),
            "portal_type=imio.directory.Contact",
        ]
        params = self.get_extra_params(params)
        url = "{}/@search?{}".format(DIRECTORY_URL, "&".join(params))
        return url


class DirectoryEndpointGet(Service):
    def render(self):
        related_items = DirectoryEndpoint(self.context, self.request)
        return json.dumps(
            related_items(),
            indent=2,
            sort_keys=True,
            separators=(", ", ": "),
        )
