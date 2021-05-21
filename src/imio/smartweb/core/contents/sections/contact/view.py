# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.views import SectionView
from imio.smartweb.core.utils import get_directory_json
from plone import api


class ContactView(SectionView):
    """Contact Section view"""

    @property
    def contact(self):
        smartweb_directory_url = api.portal.get_registry_record("imio.directory.url")
        url = "{}/@search?UID={}&fullobjects=1".format(
            smartweb_directory_url, self.context.related_contact
        )
        json_search_contact = get_directory_json(url)
        if (
            json_search_contact is None
            or len(json_search_contact.get("items", [])) == 0  # NOQA
        ):
            return
        return json_search_contact.get("items")[0]

    @property
    def images(self):
        contact = self.contact
        if contact is None:
            return
        contact_url = contact["@id"]
        query = "@search?portal_type=Image&path.depth=1"
        images_url_request = "{}/{}".format(contact_url, query)
        json_images = get_directory_json(images_url_request)
        if json_images is None or len(json_images.get("items", [])) == 0:
            return
        return json_images.get("items")
