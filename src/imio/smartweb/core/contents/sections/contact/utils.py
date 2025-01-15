# -*- coding: utf-8 -*-

from imio.smartweb.common.contact_utils import ContactProperties as ContactSchedule
from imio.smartweb.common.utils import rich_description
from imio.smartweb.core.utils import batch_results
from imio.smartweb.core.utils import get_json
from imio.smartweb.core.utils import hash_md5
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from zope.i18n import translate

import json


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
        country = (
            self.contact.get("country")
            and self.contact.get("country").get("title")
            or ""
        )
        if not (street or entity or country):
            return None
        return {"street": street, "entity": entity, "country": country}

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
