# -*- coding: utf-8 -*-
from datetime import datetime
from imio.smartweb.core.utils import get_json
from imio.smartweb.locales import SmartwebMessageFactory as _
from imio.smartweb.core.contents.rest.view import BaseRestView
from imio.smartweb.core.interfaces import IOgpViewUtils
from plone import api
from zope.interface import implementer


@implementer(IOgpViewUtils)
class EventsViewView(BaseRestView):
    """EventsView view"""

    @property
    def propose_url(self):
        return api.portal.get_registry_record("smartweb.propose_events_url")

    @property
    def display_map(self):
        return self.context.display_map

    @property
    def only_past_events(self):
        return self.context.only_past_events

    @property
    def display_agendas_titles(self):
        return self.context.display_agendas_titles

    @property
    def show_categories_or_topics(self):
        return self.context.show_categories_or_topics

    @property
    def event(self):
        event = self._formated_event(self.item)
        return event

    def _formated_event(self, data):
        current_lang = api.portal.get_current_language()[:2]

        # Récupération des données de base
        name = data.get(f"title_{current_lang}") or data.get("title")
        text = data.get(f"text_{current_lang}") or data.get("text")
        description = data.get(f"description_{current_lang}") or data.get("description")
        number = data.get("number")
        street = data.get("street")
        city = data.get("city")
        zipcode = data.get("zipcode")
        country = data.get("country").get("title") if data.get("country") else None
        full_address = self._format_address(street, number, zipcode, city, country)
        phone = data.get("contact_phone")
        email = data.get("contact_email")
        event_url = data.get("event_url")
        event_type = (
            data.get("event_type", {}).get("title", "")
            if data.get("event_type")
            else None
        )

        # Dates management
        start_date = data.get("start")
        end_date = data.get("end")
        start_date_obj = datetime.fromisoformat(start_date)
        end_date_obj = datetime.fromisoformat(end_date)
        whole_day = data.get("whole_day", False)
        if whole_day:
            formatted_date = start_date_obj.date().strftime("%d/%m/%Y")
            wd = _(f"Whole day")
            display_period_text = _(f"{formatted_date} ({wd})")
        else:
            formatted_start = start_date_obj.strftime("%d/%m/%Y %H:%M")
            formatted_end = end_date_obj.strftime("%d/%m/%Y %H:%M")
            display_period_text = f"{formatted_start} - {formatted_end}"

        # Geolocation
        geo = data.get("geolocation") or {}
        latitude, longitude = geo.get("latitude"), geo.get("longitude")

        if not latitude or not longitude:
            geo = None
            latitude = longitude = None

        # Picture
        image_info = data.get("image") or {}
        image_url = None

        # Choisir dynamiquement la scale 'portrait_affiche' si disponible
        if "scales" in image_info and "portrait_affiche" in image_info["scales"]:
            image_url = image_info["scales"]["portrait_affiche"]["download"]
        elif "download" in image_info:
            # Fallback sur l'image originale
            image_url = image_info["download"]

        if not data:
            return None
        # Construction du JSON simplifié
        prefix_address = _("Address")
        prefix_email = _("Email")
        prefix_description = _("Description")
        prefix_category = _("Event category")
        prefix_type = _("Event type")
        event = {
            "name": name,
            "text": text,
            "address": f"{prefix_address}: {full_address}" if full_address else None,
            "phone": phone,
            "email": f"{prefix_email}: {email}" if email else None,
            "description": (
                f"{prefix_description}: {description}" if description else None
            ),
            "url": event_url,
            "geolocation": (latitude, longitude) if geo else None,
            "event_type": f"{prefix_type}: {event_type}" if event_type else None,
            "image_url": image_url if image_url else None,
            "period_text": display_period_text,
            "start_date": start_date_obj.strftime("%d/%m/%Y %H:%M"),
            "end_date": end_date_obj.strftime("%d/%m/%Y %H:%M"),
        }
        return event
