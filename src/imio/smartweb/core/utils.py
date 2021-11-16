# -*- coding: utf-8 -*-

from collective.taxonomy.interfaces import ITaxonomy
from imio.smartweb.core.config import WCA_URL
from more_itertools import chunked
from plone import api
from Products.CMFPlone.utils import base_hasattr
from zope.component import getSiteManager

import json
import os
import requests


def get_category(context):
    if not base_hasattr(context, "category_name"):
        return
    field_name = "taxonomy_{}".format(context.category_name)
    taxonomy_name = "collective.taxonomy.{}".format(context.category_name)
    term = getattr(context, field_name)
    if not term:
        return
    current_lang = api.portal.get_current_language()[:2]
    sm = getSiteManager()
    utility = sm.queryUtility(ITaxonomy, name=taxonomy_name)
    value = utility.translate(
        term,
        context=context,
        target_language=current_lang,
    )
    return value


def get_categories():
    sm = getSiteManager()
    return sm.queryUtility(ITaxonomy, name="collective.taxonomy.page_category")


def concat_voca_term(term1, term2):
    return "{0}-{1}".format(term1, term2)


def concat_voca_title(title1, title2):
    return "{0} - {1}".format(title1, title2)


def get_json(url, auth=None):
    headers = {"Accept": "application/json"}
    if auth is not None:
        headers["Authorization"] = auth
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except Exception:
        return None
    if response.status_code != 200:
        return None
    return json.loads(response.text)


def get_wca_token(client_id, client_secret):
    payload = {
        "grant_type": "password",
        "client_id": client_id,
        "client_secret": client_secret,
        "username": os.environ.get("RESTAPI_USER_USERNAME"),
        "password": os.environ.get("RESTAPI_USER_PASSWORD"),
        "scope": ["openid"],
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    response = requests.post(WCA_URL, headers=headers, data=payload)
    id_token = response.json().get("id_token")
    return id_token


def safe_html(html):
    if not html:
        return
    transforms = api.portal.get_tool("portal_transforms")
    data = transforms.convertTo(target_mimetype="text/x-html-safe", orig=html)
    output = data.getData()
    return output


def batch_results(iterable, batch_size):
    return list(chunked(iterable, batch_size, strict=False))
