# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.views import SectionView
from imio.smartweb.core.utils import get_directory_json


class ContactView(SectionView):
    """Contact Section view"""

    @property
    def contact(self):
        contact_url = self.context.related_contact
        json_contact = get_directory_json(contact_url)
        if json_contact is None or len(json_contact.get("items", [])) == 0:
            return
        return json_contact.get("items")

    @property
    def images(self):
        contact_url = self.context.related_contact
        query = "@search?portal_type=Image&path.depth=1"
        images_url_request = "{}/{}".format(contact_url, query)
        json_images = get_directory_json(images_url_request)
        if json_images is None or len(json_images.get("items", [])) == 0:
            return
        return json_images.get("items")
