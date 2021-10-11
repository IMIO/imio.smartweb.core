# -*- coding: utf-8 -*-

from plone.restapi.search.handler import SearchHandler
from plone.restapi.search.utils import unflatten_dotted_dict
from plone.restapi.services import Service
from plone import api

import pkg_resources

try:
    pkg_resources.get_distribution("collective.solr")
    HAS_SOLR = True
    from collective.solr.search import Search
except pkg_resources.DistributionNotFound:
    HAS_SOLR = False


class SearchGet(Service):
    def reply(self):
        query = self.request.form.copy()
        query = unflatten_dotted_dict(query)
        return ExtendedSearchHandler(self.context, self.request).search(query)


class ExtendedSearchHandler(SearchHandler):
    def search(self, query):
        if "_core" in query:
            parameters = self._core_query(query["_core"])
            del query["_core"]
            if parameters:
                query.update(parameters)
        return super(ExtendedSearchHandler, self).search(query)

    def _core_query(self, core):
        parameters = {
            "news": {
                "portal_type": ["imio.news.NewsItem"],
            },
            "events": {
                "portal_type": ["imio.events.Event"],
            },
            "directory": {
                "portal_type": ["imio.directory.Contact"],
            },
        }.get(core)

        if parameters:
            if HAS_SOLR is True:
                entity_uid = api.portal.get_registry_record(
                    "smartweb.{0}_entity_uid".format(core)
                )
                results = Search().search('UID:"{0}"'.format(entity_uid), core=core)
                if results:
                    parameters["path"] = results[0].path_string
            parameters["core"] = api.portal.get_registry_record(
                "smartweb.{0}_solr_core".format(core)
            )
        return parameters
