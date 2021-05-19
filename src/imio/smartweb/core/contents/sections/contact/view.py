# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.views import SectionView
from zope.schema.vocabulary import SimpleVocabulary
import json
import requests


class ContactView(SectionView):
    """Contact Section view"""

    @property
    def contact(self):
        try:
            response = requests.get(
                self.context.related_contact, headers={"Accept": "application/json"}
            )
        except Exception:
            return
        if response.status_code != 200:
            return
        json_contact = json.loads(response.text)
        if len(json_contact.get("items", [])) == 0:
            return
        return json_contact.get("items")

    @property
    def images(self):
        try:
            contact_url = self.context.related_contact
            images_url_request = "{}/@search?portal_type=Image&path.depth=1".format(contact_url)
            response = requests.get(
                images_url_request, headers={"Accept": "application/json"}
            )
        except Exception:
            return
        if response.status_code != 200:
            return
        json_images = json.loads(response.text)
        if len(json_images.get("items", [])) == 0:
            return
        return json_images.get("items")

