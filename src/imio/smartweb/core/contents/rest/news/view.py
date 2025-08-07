# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.rest.view import BaseRestView
from imio.smartweb.core.interfaces import IOgpViewUtils
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from zope.interface import implementer


@implementer(IOgpViewUtils)
class NewsViewView(BaseRestView):
    """NewsView view"""

    @property
    def propose_url(self):
        return api.portal.get_registry_record("smartweb.propose_news_url")

    @property
    def display_newsfolders_titles(self):
        return self.context.display_newsfolders_titles

    @property
    def show_categories_or_topics(self):
        return self.context.show_categories_or_topics

    @property
    def news(self):
        news = self._formated_news(self.item)
        return news

    def _formated_news(self, data):
        current_lang = api.portal.get_current_language()[:2]
        # Récupération des données de base
        name = data.get(f"title_{current_lang}") or data.get("title")
        text = data.get(f"text_{current_lang}") or data.get("text")
        description = data.get(f"description_{current_lang}") or data.get("description")
        phone = data.get("contact_phone")
        email = data.get("contact_email")
        url = data.get("site_url")

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
        prefix_email = _("Email")
        prefix_description = _("Description")
        news = {
            "name": name,
            "text": text,
            "phone": phone,
            "email": f"{prefix_email}: {email}" if email else None,
            "description": (
                f"{prefix_description}: {description}" if description else None
            ),
            "url": url,
            "image_url": image_url if image_url else None,
        }
        return news
