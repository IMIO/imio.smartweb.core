# -*- coding: utf-8 -*-
from imio.smartweb.core.config import DIRECTORY_URL
from imio.smartweb.locales import SmartwebMessageFactory as _
from imio.smartweb.core.utils import get_json
from imio.smartweb.core.contents.rest.view import BaseRestView
from imio.smartweb.core.interfaces import IOgpViewUtils
from plone import api
from urllib.parse import parse_qs
from zope.interface import implementer


@implementer(IOgpViewUtils)
class DirectoryViewView(BaseRestView):
    """DirectoryView view"""

    @property
    def propose_url(self):
        return api.portal.get_registry_record("smartweb.propose_directory_url")

    @property
    def display_map(self):
        return self.context.display_map

    @property
    def contact(self):
        contact = self._formated_contact(self.item)
        return contact

    def _formated_contact(self, data):
        current_lang = api.portal.get_current_language()[:2]

        # Récupération des données de base
        name = data.get(f"title_{current_lang}") or data.get("title")
        subtitle = data.get(f"subtitle_{current_lang}") or data.get("subtitle")
        number = data.get("number")
        street = data.get("street")
        city = data.get("city")
        zipcode = data.get("zipcode")
        country = data.get("country").get("title") if data.get("country") else None
        full_address = self._format_address(street, number, zipcode, city, country)

        # Téléphone (premier numéro s’il existe)
        phone = None
        if data.get("phones"):
            phone = data["phones"][0].get("number")

        # Email (première adresse s’il existe)
        email = None
        if data.get("mails"):
            email = data["mails"][0].get("mail_address")

        # URL (premier lien s’il existe)
        url = None
        if data.get("urls"):
            url = data["urls"][0].get("url")

        # Description (française en priorité)
        description = data.get(f"description_{current_lang}") or data.get("description")

        # Catégorie
        category = None
        if data.get("taxonomy_contact_category"):
            category = data["taxonomy_contact_category"][0].get("title")

        # Type
        contact_type = data.get("type", {}).get("title")

        # Géolocalisation
        geo = data.get("geolocation") or {}
        latitude = geo.get("latitude")
        longitude = geo.get("longitude")

        # Picture
        image_info = data.get("image") or {}
        image_url = None

        # Choisir dynamiquement la scale 'portrait_affiche' si disponible
        if "scales" in image_info and "portrait_affiche" in image_info["scales"]:
            image_url = image_info["scales"]["portrait_affiche"]["download"]
        elif "download" in image_info:
            # Fallback sur l'image originale
            image_url = image_info["download"]

        # Construction du JSON simplifié
        prefix_address = _("Address")
        prefix_email = _("Email")
        prefix_description = _("Description")
        prefix_category = _("Contact category")
        prefix_type = _("Contact type")
        contact = {
            "name": name,
            "subtitle": subtitle,
            "address": f"{prefix_address}: {full_address}" if full_address else None,
            "phone": phone,
            "email": f"{prefix_email}: {email}" if email else None,
            "description": (
                f"{prefix_description}: {description}" if description else None
            ),
            "url": url,
            "category": f"{prefix_category}: {category}" if category else None,
            "geolocation": (latitude, longitude) if geo else None,
            "contact_type": f"{prefix_type}: {contact_type}" if contact_type else None,
            "image_url": image_url if image_url else None,
        }
        return contact
