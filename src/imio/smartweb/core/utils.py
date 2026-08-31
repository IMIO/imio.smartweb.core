# -*- coding: utf-8 -*-

from AccessControl import Unauthorized
from Acquisition import aq_parent
from collective.taxonomy.interfaces import ITaxonomy
from imio.smartweb.core.config import EVENTS_URL
from imio.smartweb.core.config import NEWS_URL
from imio.smartweb.core.contents import IFolder
from more_itertools import chunked
from plone import api
from plone.app.multilingual.interfaces import ILanguageRootFolder
from plone.dexterity.interfaces import IDexterityContent
from plone.memoize import ram
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.defaultpage import get_default_page
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Products.CMFPlone.utils import base_hasattr
from time import time
from urllib.parse import urlparse, urlunparse
from zope.component import getSiteManager
from zope.component import getUtility
from zope.component import queryMultiAdapter
from zope.globalrequest import getRequest

import base64
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
    language = api.portal.get_current_language()
    headers = {"Accept": "application/json", "Cookie": f"I18N_LANGUAGE={language}"}
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
    if response.text:
        return json.loads(response.text)


def get_wca_token(client_id, client_secret):
    username = os.environ.get(
        "SSO_APPS_USER_USERNAME", "imio-apps-smartweb_belleville-ac"
    )
    password = os.environ.get("SSO_APPS_USER_PASSWORD", "")

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
    sso_apps_url = os.environ.get(
        "SSO_APPS_URL",
        "https://keycloak.127.0.0.1.nip.io/realms/imio/protocol/openid-connect/token",
    )
    response = requests.post(sso_apps_url, headers=headers, data=payload, timeout=10)
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


def reindexParent(obj, event=None):
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
        image_field = getattr(context, fieldname, None)
        if image_field and getattr(image_field, "contentType", "") == "image/svg+xml":
            # SVG images cannot be scaled by PIL — return the original file URL
            modified_hash = hash_md5(context.ModificationDate())
            return f"{context.absolute_url()}/@@images/{fieldname}?cache_key={modified_hash}"
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


def get_value_from_registry(key):
    val = api.portal.get_registry_record(key)
    return val


def get_iadeliberation_url_from_registry():
    iadeliberation_url = api.portal.get_registry_record("smartweb.iadeliberations_url")
    return iadeliberation_url


def get_iadeliberation_institution_from_registry():
    iadeliberation_institution = api.portal.get_registry_record(
        "smartweb.iadeliberations_institution"
    )
    return iadeliberation_institution


def get_iadeliberation_json(url):
    iadeliberation_user = api.portal.get_registry_record(
        "smartweb.iadeliberations_api_username"
    )
    iadeliberation_pwd = api.portal.get_registry_record(
        "smartweb.iadeliberation_api_password"
    )
    usrPass = f"{iadeliberation_user}:{iadeliberation_pwd}".encode("utf-8")
    b64Val = base64.b64encode(usrPass)
    json = get_json(url, auth=f"Basic {b64Val.decode('utf-8')}", timeout=20)

    return json


def get_iaideabox_json(url):
    user = api.portal.get_registry_record("smartweb.iaideabox_api_username")
    pwd = api.portal.get_registry_record("smartweb.iaideabox_api_password")
    usrPass = f"{user}:{pwd}".encode("utf-8")
    b64Val = base64.b64encode(usrPass)
    json = get_json(url, auth=f"Basic {b64Val.decode('utf-8')}", timeout=20)
    return json


def get_basic_auth_json(url, user, pwd):
    usrPass = f"{user}:{pwd}".encode("utf-8")
    b64Val = base64.b64encode(usrPass)
    json = get_json(url, auth=f"Basic {b64Val.decode('utf-8')}", timeout=20)
    return json


def is_valid_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        return all([parsed.scheme in ("http", "https"), parsed.netloc])
    except Exception:
        return False


def get_ts_api_url(service="wcs"):
    url_ts = get_value_from_registry("smartweb.url_ts")
    if url_ts is None:
        return None
    if not is_valid_url(url_ts):
        return None
    parsed_url = urlparse(url_ts)
    if "wcs" in service:
        new_netloc = parsed_url.netloc.replace(
            ".guichet-citoyen.be", "-formulaires.guichet-citoyen.be"
        )
    api_url = urlunparse(parsed_url._replace(netloc=new_netloc, path="/api"))
    return api_url


def remove_cache_key(json_data: dict) -> dict:
    pattern = re.compile(r"&cache_key=[a-f0-9]{32}")
    if json_data is None:
        return json_data
    if "@id" in json_data and isinstance(json_data["@id"], str):
        json_data["@id"] = pattern.sub("", json_data["@id"])

    # Nested keys inside 'batching'
    if "batching" in json_data and isinstance(json_data["batching"], dict):
        for key in ["@id", "first", "last", "next"]:
            if key in json_data["batching"] and isinstance(
                json_data["batching"][key], str
            ):
                json_data["batching"][key] = pattern.sub("", json_data["batching"][key])

    return json_data


def populate_procedure_button_text():
    """Populate the procedure_button_text in the control panel registry."""
    registry = getUtility(IRegistry)
    # if not registry.get("smartweb.procedure_button_text", None):
    #     logger.info("Populating smartweb.procedure_button_text in registry")
    registry["smartweb.procedure_button_text"] = [
        {
            "label_id": "label-1",
            "label_fr": "Effectuer cette démarche en ligne",
            "label_nl": "Voltooi deze procedure online",
            "label_de": "Diese Prozedur online abschließen",
            "label_en": "Complete this procedure online",
        },
        {
            "label_id": "label-2",
            "label_fr": "Postuler",
            "label_nl": "Solliciteren",
            "label_de": "Bewerben",
            "label_en": "Apply",
        },
    ]


class ScopeUnavailable(Exception):
    """The scope of an agenda or a news folder could not be determined.

    Raised inside the cached fetch so that ``ram.cache`` stores nothing: an
    exception never reaches its ``cache[key] = fun(...)`` assignment.
    """


def _fetch_scope(base_url, uid, populating_key):
    """The two requests behind a scope lookup, shared by agendas and folders.

    The catalog summary resolves the object's URL from its UID, then the object
    itself carries its ``populating_*`` list (the summary does not).
    """
    listing = get_json(f"{base_url}/@search?UID={uid}&metadata_fields=UID")
    items = (listing or {}).get("items") or []
    if not items:
        raise ScopeUnavailable(uid)
    container = get_json(items[0]["@id"]) or {}
    if not container.get("UID"):
        raise ScopeUnavailable(uid)
    scope = [(container["UID"], container.get("title", ""))]
    for populating in container.get(populating_key) or []:
        scope.append((populating["UID"], populating.get("title", "")))
    return scope


def _agenda_scope_cache_key(func, agenda_uid):
    return ("agenda", agenda_uid, time() // (60 * 5))


def _newsfolder_scope_cache_key(func, newsfolder_uid):
    return ("newsfolder", newsfolder_uid, time() // (60 * 5))


@ram.cache(_agenda_scope_cache_key)
def _fetch_agenda_scope(agenda_uid):
    return _fetch_scope(EVENTS_URL, agenda_uid, "populating_agendas")


@ram.cache(_newsfolder_scope_cache_key)
def _fetch_newsfolder_scope(newsfolder_uid):
    return _fetch_scope(NEWS_URL, newsfolder_uid, "populating_newsfolders")


def get_agenda_scope(agenda_uid):
    """(uid, title) of an agenda and of every agenda populating it.

    That list is what an EventsView displaying this agenda is able to show,
    because the authentic source applies the cascade itself.

    Only a *successful* answer is cached: caching a remote outage would turn a
    one-second blip into five minutes of empty dropdowns for every editor.
    """
    if not agenda_uid:
        return []
    try:
        return _fetch_agenda_scope(agenda_uid)
    except ScopeUnavailable:
        return []


def get_newsfolder_scope(newsfolder_uid):
    """(uid, title) of a news folder and of every folder populating it.

    The mirror of ``get_agenda_scope()``, same caching rule.
    """
    if not newsfolder_uid:
        return []
    try:
        return _fetch_newsfolder_scope(newsfolder_uid)
    except ScopeUnavailable:
        return []


def get_agenda_scope_uids(agenda_uid):
    """UIDs of the agendas an EventsView on ``agenda_uid`` is able to display.

    Hands back the raw list rather than answering "is this in scope?": an empty
    scope means the remote could not be reached, never "nothing is in scope",
    so callers must guard their check with ``scope and ...``.
    """
    return [uid for uid, title in get_agenda_scope(agenda_uid)]


def get_newsfolder_scope_uids(newsfolder_uid):
    """UIDs of the folders a NewsView on ``newsfolder_uid`` is able to display.

    See ``get_agenda_scope_uids()`` for why the empty case stays visible.
    """
    return [uid for uid, title in get_newsfolder_scope(newsfolder_uid)]


def get_linking_rest_view(context, portal_type):
    """The rest view a section links to, preferring what the form submits.

    A vocabulary only ever receives the *context*, so on an add form it would
    see no linking view and scope everything to nothing. The submitted value is
    read first, under both keys it can arrive by: the AJAX widget sends
    ``linking_rest_view``, a form POST sends ``form.widgets.linking_rest_view``.

    Resolved with the editor's own permissions, like ``@@scoped-agendas``: the
    two must agree or the cascade would empty a ``<select>`` the server accepts.
    """
    request = getRequest()
    raw = None
    if request is not None:
        raw = request.form.get("linking_rest_view") or request.form.get(
            "form.widgets.linking_rest_view"
        )
    if isinstance(raw, (list, tuple)):
        raw = raw[0] if raw else None
    if raw:
        # the contentbrowser stores one or more UIDs separated by ";"
        uid = str(raw).split(";")[0].strip()
        if uid:
            try:
                rest_view = api.content.get(UID=uid)
            except Unauthorized:
                rest_view = None
            if getattr(rest_view, "portal_type", None) == portal_type:
                return rest_view
    linking_rest_view = getattr(context, "linking_rest_view", None)
    # On a real submission this is the view itself, not a RelationValue (see
    # RelationChoiceContentBrowserWidgetConverter.toFieldValue). Both shapes.
    rest_view = getattr(linking_rest_view, "to_object", linking_rest_view)
    if getattr(rest_view, "portal_type", None) == portal_type:
        return rest_view
    return None


def get_linking_events_view(context):
    """The EventsView a section links to. See get_linking_rest_view()."""
    return get_linking_rest_view(context, "imio.smartweb.EventsView")
