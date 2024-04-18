# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from Acquisition import aq_parent
from collective.taxonomy.interfaces import ITaxonomy
from imio.smartweb.core.config import WCA_URL
from imio.smartweb.core.contents import IFolder
from more_itertools import chunked
from plone import api
from plone.app.multilingual.interfaces import ILanguageRootFolder
from plone.dexterity.interfaces import IDexterityContent
from Products.CMFPlone.defaultpage import get_default_page
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Products.CMFPlone.utils import base_hasattr
from zope.component import getSiteManager
from zope.component import queryMultiAdapter
from zope.globalrequest import getRequest

import hashlib
import json
import logging
import os
import re
import requests

logger = logging.getLogger("imio.smartweb.core")


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


def get_json(url, auth=None, timeout=5):
    headers = {"Accept": "application/json"}
    if auth is not None:
        headers["Authorization"] = auth
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
    except requests.exceptions.Timeout:
        logger.warning(f"Timeout raised for requests : {url}")
        return None
    except Exception:
        return None
    if response.status_code != 200:
        return None
    return json.loads(response.text)


def get_wca_token(client_id, client_secret):
    username = os.environ.get("RESTAPI_USER_USERNAME")
    password = os.environ.get("RESTAPI_USER_PASSWORD")

    payload = {
        "grant_type": "password",
        "client_id": client_id,
        "client_secret": client_secret,
        "username": username,
        "password": password,
        "scope": ["openid"],
    }
    if not client_id or not client_secret:
        return (username, password)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    response = requests.post(WCA_URL, headers=headers, data=payload)
    id_token = response.json().get("id_token")
    return "Bearer {0}".format(id_token)


def hash_md5(text):
    return hashlib.md5(text.encode()).hexdigest()


def safe_html(html):
    if not html:
        return
    transforms = api.portal.get_tool("portal_transforms")
    data = transforms.convertTo(target_mimetype="text/x-html-safe", orig=html)
    output = data.getData()
    return output


def batch_results(iterable, batch_size):
    return list(chunked(iterable, batch_size, strict=False))


def reindexParent(obj, event):
    parent = aq_parent(obj)
    if parent is not None:
        # in some cases (ex: relation breaking), we do not get the object in
        # its acquisition chain
        parent.reindexObject()


def get_default_content_id(obj):
    if IPloneSiteRoot.providedBy(obj) or ILanguageRootFolder.providedBy(obj):
        # Plone / LRF default page
        item_id = get_default_page(obj)
        return item_id and item_id or ""
    elif IFolder.providedBy(obj):
        # Our folder default page
        item = obj.get_default_item()
        return item and item.getId or ""


def get_scale_url(context, request, fieldname, scale_name, orientation=""):
    if orientation:
        m = re.match(r"(portrait|paysage|carre)_(\w+)", scale_name)
        if m:
            # remove existing orientation (if any) from scale name
            scale_name = m.group(2)
    scale_name = "_".join(filter(None, [orientation, scale_name]))
    if IDexterityContent.providedBy(context):
        # get scale url on an object
        if not scale_name:
            # return the full image
            modified_hash = hash_md5(context.ModificationDate())
            return f"{context.absolute_url()}/@@images/{fieldname}/?cache_key={modified_hash}"
        images_view = queryMultiAdapter((context, request), name="images")
        if images_view is None:
            return ""
        scale = images_view.scale(fieldname, scale_name)
        if scale is None:
            return ""
        return scale.url
    else:
        # get scale url on a brain
        # In this case, we need a modification hash to handle croppings, because
        # catalog does not handle them correctly.
        # See https://github.com/collective/plone.app.imagecropping/issues/129
        brain = context
        if fieldname == "image" and not brain.has_leadimage:
            return ""
        modification_date = brain.ModificationDate
        if callable(modification_date):
            # brain in content listing for example
            modification_date = modification_date()
        modified_hash = hash_md5(modification_date)
        url = f"{brain.getURL()}/@@images/{fieldname}/{scale_name}?cache_key={modified_hash}"
        return url


def get_plausible_vars():
    env_plausible_url = os.getenv("SMARTWEB_PLAUSIBLE_URL", "")
    env_plausible_site = os.getenv("SMARTWEB_PLAUSIBLE_SITE", "")
    env_plausible_token = os.getenv("SMARTWEB_PLAUSIBLE_TOKEN", "")

    plausible_url = (
        env_plausible_url
        if (env_plausible_url and env_plausible_url != "")
        else api.portal.get_registry_record("smartweb.plausible_url")
    )
    plausible_site = (
        env_plausible_site
        if (env_plausible_site and env_plausible_site != "")
        else api.portal.get_registry_record("smartweb.plausible_site")
    )
    plausible_token = (
        env_plausible_token
        if (env_plausible_token and env_plausible_token != "")
        else api.portal.get_registry_record("smartweb.plausible_token")
    )
    if all([plausible_site, plausible_url, plausible_token]):
        plausible_vars = {
            "plausible_url": plausible_url,
            "plausible_site": plausible_site,
            "plausible_token": plausible_token,
        }
        return plausible_vars
    else:
        return None


def get_current_language(context=None):
    """Return the current negotiated language.

    :param context: context object
    :type context: object
    :returns: language identifier
    :rtype: string
    :Example: :ref:`portal-get-current-language-example`
    """
    request = getRequest()
    if request is None:
        return (
            context and aq_inner(context).Language()
        ) or api.portal.get_default_language()
    return (
        request.get("LANGUAGE", None)
        or (context and aq_inner(context).Language())
        or api.portal.get_default_language()
    )
