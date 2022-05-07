# -*- coding: utf-8 -*-

from datetime import datetime
from imio.smartweb.core.config import DIRECTORY_URL
from imio.smartweb.core.config import EVENTS_URL
from imio.smartweb.core.config import NEWS_URL
from plone import api
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.memoize import ram
from plone.restapi.search.handler import SearchHandler
from plone.restapi.search.utils import unflatten_dotted_dict
from plone.restapi.services import Service
from time import time


def _cache_key(func, navigation_root):
    uid_method = getattr(navigation_root, "UID", None)
    uid = uid_method and uid_method() or "PloneSite"
    return (uid, time() // (5 * 60))


@ram.cache(_cache_key)
def get_news_views(navigation_root):
    with api.env.adopt_user(username="admin"):
        brains = api.content.find(
            context=navigation_root, portal_type="imio.smartweb.NewsView"
        )
        # Can be improved by using index
        return {b.getObject().selected_news_folder: b.getURL() for b in brains}


@ram.cache(_cache_key)
def get_events_views(navigation_root):
    with api.env.adopt_user(username="admin"):
        brains = api.content.find(
            context=navigation_root, portal_type="imio.smartweb.EventsView"
        )
        # Can be improved by using index
        return {b.getObject().selected_agenda: b.getURL() for b in brains}


def get_navigation_root(context):
    """Return given context navigation root"""
    if INavigationRoot.providedBy(context):
        return context
    else:
        for item in context.aq_chain:
            if INavigationRoot.providedBy(item):
                return item


def get_default_view_url(view_type):
    record = api.portal.get_registry_record(
        "smartweb.default_{0}_view".format(view_type), default=None
    )
    if not record:
        return ""
    with api.env.adopt_user(username="admin"):
        return api.content.get(UID=record).absolute_url()


def get_views_mapping(navigation_root):
    news = get_news_views(navigation_root)
    news["default"] = get_default_view_url("news")

    events = get_events_views(navigation_root)
    events["default"] = get_default_view_url("events")

    # Directory is a special usecase, since there is no selected entity
    # the global entity must be used
    default_directory_view = get_default_view_url("directory")
    directory_entity_uid = api.portal.get_registry_record(
        "smartweb.directory_entity_uid"
    )
    directory = {
        directory_entity_uid: default_directory_view,
        "default": default_directory_view,
    }

    mapping = {
        "imio.news.NewsItem": news,
        "imio.events.Event": events,
        "imio.directory.Contact": directory,
    }
    return mapping


class SearchGet(Service):
    def reply(self):
        query = self.request.form.copy()
        query = unflatten_dotted_dict(query)
        return ExtendedSearchHandler(self.context, self.request).search(query)


class ExtendedSearchHandler(SearchHandler):
    def search(self, query):
        if "_core" not in query and "use_site_search_settings" not in query:
            # Use site search settings by default only for current site search
            query["use_site_search_settings"] = True
        if "use_solr" not in query:
            query["use_solr"] = True  # enforce use of SolR by default
        if "_core" in query:
            parameters = self._core_query(query["_core"])
            del query["_core"]
            if parameters:
                if "metadata_fields" in query:
                    parameters["metadata_fields"] = self._update_metadata_fields(
                        query["metadata_fields"],
                        parameters["metadata_fields"],
                    )
                self.request.form["metadata_fields"] = parameters["metadata_fields"]
                query.update(parameters)
        result = super(ExtendedSearchHandler, self).search(query)
        if "core" in query:
            return self._adapt_result(result, query["core"])
        return result

    def _get_source_url(self, path, core):
        base_urls = {
            "directory": DIRECTORY_URL,
            "news": NEWS_URL,
            "events": EVENTS_URL,
        }
        return "{0}/{1}".format(base_urls.get(core, ""), "/".join(path.split("/")[2:]))

    def _adapt_result(self, result, core):
        """Transform result"""
        mapping = get_views_mapping(self._navigation_root)
        result["items"] = [
            self._adapt_result_url(i, mapping, core) for i in result["items"]
        ]
        return result

    def _adapt_result_url(self, item, mapping, core):
        """Ensure that url to external objects are adapted based on react views"""
        if item["@type"] not in mapping:
            return item
        type_mapping = mapping[item["@type"]]
        base_url = type_mapping.get(item["container_uid"], type_mapping["default"])
        item["_url"] = "{base}#/content?u={item_uid}".format(
            base=base_url,
            item_uid=item["UID"],
        )
        item["_source_url"] = self._get_source_url(item["path_string"], core)
        return item

    @property
    def _navigation_root(self):
        return get_navigation_root(self.context)

    def _update_metadata_fields(self, original, new):
        if isinstance(original, str):
            original = [original]
        return [*original, *[e for e in new if e not in original]]

    def _core_query(self, core):
        """Return core specific query parameters"""
        mapping = get_views_mapping(self._navigation_root)
        parameters = {
            "news": {
                "portal_type": ["imio.news.NewsItem"],
                "metadata_fields": [
                    "id",
                    "UID",
                    "container_uid",
                    "has_leadimage",
                    "path_string",
                ],
                "selected_news_folders": {
                    "query": [
                        k
                        for k in mapping["imio.news.NewsItem"].keys()
                        if k != "default"
                    ],
                    "operator": "or",
                },
                "expires": {"query": datetime.now(), "range": "min"},
                "path": "",
            },
            "events": {
                "portal_type": ["imio.events.Event"],
                "metadata_fields": [
                    "id",
                    "UID",
                    "container_uid",
                    "has_leadimage",
                    "path_string",
                ],
                "selected_agendas": {
                    "query": [
                        k for k in mapping["imio.events.Event"].keys() if k != "default"
                    ],
                    "operator": "or",
                },
                "event_dates": {"query": datetime.now().date(), "range": "min"},
                "expires": {"query": datetime.now(), "range": "min"},
                "path": "",
            },
            "directory": {
                "portal_type": ["imio.directory.Contact"],
                "metadata_fields": [
                    "id",
                    "UID",
                    "container_uid",
                    "has_leadimage",
                    "path_string",
                ],
                "selected_entities": {
                    "query": [
                        k
                        for k in mapping["imio.directory.Contact"].keys()
                        if k != "default"
                    ],
                    "operator": "or",
                },
                "expires": {"query": datetime.now(), "range": "min"},
                "path": "",
            },
        }.get(core)

        required_fields = {
            "news": "selected_news_folders",
            "events": "selected_agendas",
            "directory": "selected_entities",
        }

        if parameters:
            parameters["core"] = api.portal.get_registry_record(
                "smartweb.{0}_solr_core".format(core)
            )
            required_field = required_fields[core]
            if not parameters.get(required_field)["query"]:
                # This avoid having unwanted results if no view was created
                parameters[required_field] = ["None"]
        return parameters
