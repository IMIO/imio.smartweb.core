# -*- coding: utf-8 -*-

from imio.smartweb.common.contact_utils import ContactProperties as ContactSchedule
from imio.smartweb.common.utils import get_term_from_vocabulary
from imio.smartweb.common.utils import rich_description
from imio.smartweb.core.config import DIRECTORY_URL
from imio.smartweb.core.utils import batch_results
from imio.smartweb.core.utils import get_json
from imio.smartweb.core.utils import hash_md5
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from zope.i18n import translate

import json

# Human labels of the remote `type` tokens. The directory owns these
# vocabularies (imio/directory/core/vocabularies.py); their msgids live in the
# shared `imio.smartweb` domain, so they can be reused here without depending
# on imio.directory.core. If the directory adds a type, its label degrades to
# the raw token -- visible but harmless.
CONTACT_TYPE_LABELS = {
    "phones": {
        "fax": _("Fax"),
        "cell": _("Mobile"),
        "home": _("Personal phone"),
        "work": _("Work phone"),
    },
    "mails": {
        "home": _("Personal email"),
        "work": _("Work email"),
    },
    "urls": {
        "facebook": _("Facebook"),
        "instagram": _("Instagram"),
        "linkedin": _("Linkedin"),
        "pinterest": _("Pinterest"),
        "twitter": _("Twitter"),
        "website": _("Website"),
        "youtube": _("Youtube"),
    },
}

# The remote column that identifies a row. A row without it cannot be keyed,
# so no preference can be recorded for it and it is skipped.
CONTACT_ROW_KEYS = {
    "phones": "number",
    "mails": "mail_address",
    "urls": "url",
}

# Columns of each row, in display order. Must mirror the *DisplayColumns
# vocabularies token for token.
CONTACT_ROW_COLUMNS = {
    "phones": ("label", "type", "number"),
    "mails": ("label", "type", "mail_address"),
    "urls": ("type", "url"),
}


def translated_type_label(kind, token):
    """Human label of a remote `type` token, or the raw token if unknown."""
    if not token:
        return ""
    msgid = CONTACT_TYPE_LABELS.get(kind, {}).get(token)
    if msgid is None:
        return token
    current_lang = api.portal.get_current_language()[:2]
    return translate(msgid, target_language=current_lang)


def row_key(kind, row):
    """Identity of a remote row: its payload value, or "" when it has none."""
    return (row.get(CONTACT_ROW_KEYS[kind]) or "").strip()


def build_display_rows(kind, contacts, preferences=None):
    """Build the DataGridField rows of `kind` from remote contact payloads.

    `contacts` is a list of contact dicts as returned by
    `@search?UID=...&fullobjects=1`. `preferences` maps
    `(contact_uid, row_key)` to a list of column names to carry over.

    A key ABSENT from `preferences` means "no preference recorded" and yields
    every column. A key present with an EMPTY list means "explicitly hidden"
    and is kept as such. The two are not interchangeable.
    """
    preferences = preferences or {}
    all_columns = CONTACT_ROW_COLUMNS[kind]
    rows = []
    for contact in contacts:
        uid = contact.get("UID") or ""
        title = contact.get("title") or ""
        for remote_row in contact.get(kind) or []:
            key = row_key(kind, remote_row)
            if not key:
                continue
            row = {
                "contact_uid": uid,
                "contact_title": title,
                # list() so each row owns its default.
                "visible_columns": list(preferences.get((uid, key), all_columns)),
            }
            for column in all_columns:
                if column == "type":
                    row["type"] = translated_type_label(kind, remote_row.get("type"))
                else:
                    row[column] = remote_row.get(column) or ""
            rows.append(row)
    return rows


def get_remote_contacts(uids):
    """Live directory payload for `uids`, in that order.

    Deliberately uncached: this is only called from the "load contacts
    informations" button, where the editor is asking for fresh data.
    """
    if not uids:
        return []
    url = "{}/@search?UID={}&fullobjects=1".format(DIRECTORY_URL, "&UID=".join(uids))
    current_lang = api.portal.get_current_language()[:2]
    if current_lang != "fr":
        url = f"{url}&translated_in_{current_lang}=1"
    json_data = get_json(url)
    if not json_data:
        return []
    index_map = {uid: index for index, uid in enumerate(uids)}
    items = [
        item for item in json_data.get("items") or [] if item.get("UID") in index_map
    ]
    return sorted(items, key=lambda item: index_map[item["UID"]])


class ContactProperties(ContactSchedule):
    def __init__(self, json_dict, section):
        self.contact = json_dict
        self.context = section

    def __getattr__(self, name):
        return self.contact.get(name)

    @property
    def contact_type_class(self):
        contact_type = self.contact.get("type").get("token")
        return "contact-type-{}".format(contact_type)

    @property
    def description(self):
        description = rich_description(self.contact.get("description"))
        return description

    def logo(self):
        if self.contact.get("logo") is None:
            return ""
        modified_hash = hash_md5(self.contact["modified"])
        logo = f"{self.contact['@id']}/@@images/logo/preview?cache_key={modified_hash}"
        return logo

    def leadimage(self):
        if self.contact.get("image") is None:
            return ""
        modified_hash = hash_md5(self.contact["modified"])
        leadimage = f"{self.contact['@id']}/@@images/image/{self.context.orientation}_affiche?cache_key={modified_hash}"
        return leadimage

    def data_geojson(self):
        """Return the contact geolocation as GeoJSON string."""
        current_lang = api.portal.get_current_language()[:2]
        coordinates = self.contact.get("geolocation")
        longitude = coordinates.get("longitude")
        latitude = coordinates.get("latitude")
        link_text = translate(_("Itinerary"), target_language=current_lang)
        geo_json = {
            "type": "Feature",
            "properties": {
                "popup": '<a href="{}">{}</a>'.format(
                    self.get_itinerary_link(), link_text
                ),
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    longitude,
                    latitude,
                ],
            },
        }
        return json.dumps(geo_json)

    def images(self, image_scale, nb_results_by_batch):
        if "gallery" not in self.context.visible_blocks:
            return
        contact_url = self.contact["@id"]
        query = "@search?portal_type=Image&path.depth=1&metadata_fields=modified"
        images_url_request = "{}/{}".format(contact_url, query)
        json_images = get_json(images_url_request)
        if json_images is None or len(json_images.get("items", [])) == 0:
            return
        results = []
        thumb_scale = image_scale
        for image in json_images.get("items"):
            base_url = image["@id"]
            modified_hash = hash_md5(image["modified"])
            large_url = f"{base_url}/@@images/image/?cache_key={modified_hash}"
            url = f"{base_url}/@@images/image/paysage_{thumb_scale}?cache_key={modified_hash}"
            dict_item = {
                "title": image["title"],
                "description": image["description"],
                "image_large_url": large_url,
                "image_url": url,
            }
            results.append(dict_item)
        return batch_results(results, nb_results_by_batch)

    def get_itinerary_link(self):
        address_parts = [
            self.contact.get("street"),
            self.contact.get("number") and str(self.contact.get("number")) or "",
            self.contact.get("complement"),
            self.contact.get("zipcode") and str(self.contact.get("zipcode")) or "",
            self.contact.get("city"),
        ]
        if self.contact.get("country"):
            address_parts.append(self.contact.get("country").get("title"))
        address = "+".join(filter(None, address_parts))
        if not address:
            return
        return "https://www.google.com/maps/dir/?api=1&destination={}".format(address)

    def get_translated_url_type(self, url_type_id):
        current_lang = api.portal.get_current_language()[:2]
        url_type_label = url_type_id[0].upper() + url_type_id[1:]
        return translate(_(url_type_label), target_language=current_lang)

    def formatted_address(self):
        street_parts = [
            self.contact.get("street"),
            self.contact.get("number") and str(self.contact.get("number")) or "",
            self.contact.get("complement"),
        ]
        street = " ".join(filter(None, street_parts))
        entity_parts = [
            self.contact.get("zipcode") and str(self.contact.get("zipcode")) or "",
            self.contact.get("city"),
        ]
        entity = " ".join(filter(None, entity_parts))

        if self.contact.get("country"):
            country = get_term_from_vocabulary(
                "imio.smartweb.vocabulary.Countries",
                self.contact.get("country").get("token", None),
            )
            country = country.title
        else:
            country = ""
        if not (street or entity or country):
            return None
        return {"street": street, "entity": entity, "country": country}

    def translated_type(self, kind, token):
        """Human label of a remote `type` token. See translated_type_label."""
        return translated_type_label(kind, token)

    def visible_columns_map(self, kind):
        """{(contact_uid, row_key): [column, ...]} from the stored preferences.

        A key ABSENT from the returned map means "no preference recorded" and
        yields every column at render time. A key present with an EMPTY list
        means "explicitly hidden" and drops the row. The two are NOT
        interchangeable: never normalise one into the other. A stored row whose
        `visible_columns` is None is treated as "no preference", so its key is
        deliberately left out of the map.
        """
        stored = getattr(self.context, f"{kind}_display", None) or []
        result = {}
        for row in stored:
            key = row_key(kind, row)
            if not key:
                continue
            columns = row.get("visible_columns")
            if columns is None:
                continue
            result[(row.get("contact_uid") or "", key)] = list(columns)
        return result

    def displayed_rows(self, kind):
        """Remote rows of `kind`, each with the set of columns to render.

        Returns [{"data": <remote row dict>, "columns": <set of names>}, ...].
        Rows explicitly hidden are omitted, as are rows with no usable key.

        `self.contact` is the LIVE directory payload: the stored `*_display`
        data columns are residue and are never read here. The remote row dict
        is returned as-is and must not be mutated -- it belongs to cached JSON.
        """
        preferences = self.visible_columns_map(kind)
        uid = self.contact.get("UID") or ""
        all_columns = set(CONTACT_ROW_COLUMNS[kind])
        rows = []
        for remote_row in self.contact.get(kind) or []:
            key = row_key(kind, remote_row)
            if not key:
                continue
            columns = preferences.get((uid, key))
            if columns is None:
                columns = set(all_columns)
            else:
                columns = set(columns) & all_columns
                if not columns:
                    continue
            rows.append({"data": remote_row, "columns": columns})
        return rows

    @property
    def get_urls(self):
        if isinstance(self.urls, list):
            result = (
                None
                if all(
                    item["type"] is None and item["url"] is None for item in self.urls
                )
                else [
                    item
                    for item in self.urls
                    if not (item["type"] is None and item["url"] is None)
                ]
            )
        elif self.urls is None:
            result = None
        else:
            result = self.urls
        return result
