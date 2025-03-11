# # -*- coding: utf-8 -*-

from imio.smartweb.core.config import DIRECTORY_URL
from imio.smartweb.core.config import EVENTS_URL
from imio.smartweb.core.config import NEWS_URL
from imio.smartweb.core.utils import get_wca_token
from plone.memoize import ram
from time import time
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

import json
import os
import requests


def get_entity_id(vocabulary_name, uid):
    vocabulary = getUtility(IVocabularyFactory, name=vocabulary_name)()
    for term in vocabulary:
        if term.token == uid:
            return term.title or term.id
    return None


def get_auth_sources_response(
    sources_name, entity_id, wf_status=["published"], time_to_cache=60
):
    """_summary_

    Args:
        sources_name (_type_): 3 values are possible: "directory", "news", "events"
        entity_id (_type_): _description_

    Returns:
        _type_: json response
    """
    url = ""
    if sources_name == "directory":
        url = DIRECTORY_URL
        portaltype = "imio.directory.Contact"
        client_id_varname = "RESTAPI_DIRECTORY_CLIENT_ID"
        client_secret_varname = "RESTAPI_DIRECTORY_CLIENT_SECRET"
    elif sources_name == "events":
        url = EVENTS_URL
        portaltype = "imio.events.Event"
        client_id_varname = "RESTAPI_EVENTS_CLIENT_ID"
        client_secret_varname = "RESTAPI_EVENTS_CLIENT_SECRET"
    elif sources_name == "news":
        url = NEWS_URL
        portaltype = "imio.news.NewsItem"
        client_id_varname = "RESTAPI_NEWS_CLIENT_ID"
        client_secret_varname = "RESTAPI_NEWS_CLIENT_SECRET"

    payload = {
        "query": [
            {
                "i": "portal_type",
                "o": "plone.app.querystring.operation.selection.is",
                "v": [portaltype],
            },
            {
                "i": "path",
                "o": "plone.app.querystring.operation.string.absolutePath",
                "v": f"/{entity_id}",
            },
            {
                "i": "review_state",
                "o": "plone.app.querystring.operation.selection.any",
                "v": wf_status,
            },
        ],
        "metadata_fields": ["title", "modified", "id"],
        "sort_on": "effective",
        "sort_order": "descending",
        "fullobjects": False,
        "b_start": 0,
        "b_size": 4000,
    }
    client_id = os.environ.get(client_id_varname)
    client_secret = os.environ.get(client_secret_varname)
    auth = get_wca_token(client_id, client_secret)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": auth,
    }
    url = f"{url}/@querystring-search"
    response = get_cached_data(url, headers, payload, time_to_cache)
    return response


def _cache_key(func, url, headers, payload, time_to_cache):
    return (url, time() // time_to_cache)


@ram.cache(_cache_key)
def get_cached_data(url, headers, payload, time_to_cache):
    return requests.request("POST", url, headers=headers, data=json.dumps(payload))
