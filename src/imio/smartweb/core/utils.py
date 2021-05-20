# -*- coding: utf-8 -*-

from collective.taxonomy.interfaces import ITaxonomy
from plone import api
from Products.CMFPlone.utils import base_hasattr
from zope.component import getSiteManager
import json
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


def get_directory_json(url):
    try:
        response = requests.get(url, headers={"Accept": "application/json"})
    except Exception:
        return None
    if response.status_code != 200:
        return None
    return json.loads(response.text)
