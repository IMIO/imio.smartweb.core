# -*- coding: utf-8 -*-

from imio.smartweb.core.config import DIRECTORY_URL
from imio.smartweb.core.contents.sections.contact.utils import ContactProperties
from imio.smartweb.core.contents.sections.views import HashableJsonSectionView
from imio.smartweb.core.utils import batch_results
from plone import api
from zope.component import queryMultiAdapter


class ContactView(HashableJsonSectionView):
    """Contact Section view"""

    def get_number_of_contacts(self):
        """
        Returns the number of related contacts.
        """
        related_contacts = (
            self.context.related_contacts
        )  # Assurez-vous que 'related_contacts' est une liste
        if related_contacts:
            return len(related_contacts)
        return 0

    def contacts(self):
        # Firstly, try to get contact from the container view
        container_view = queryMultiAdapter(
            (self.context.aq_parent, self.request), name="full_view"
        )
        self.json_data = container_view.get_page_contacts()
        if self.json_data is None or len(self.json_data.get("items", [])) == 0:
            return []

        container_contacts = self.json_data.get("items")
        results_items = [
            contact
            for contact in container_contacts
            if contact["UID"] in self.context.related_contacts
        ]
        index_map = {
            value: index for index, value in enumerate(self.context.related_contacts)
        }
        results_items = sorted(results_items, key=lambda x: index_map[x["UID"]])

        # construct JSON data as before WEBBDC-1265 to avoid hash differences
        uids = "&UID=".join(self.context.related_contacts)
        url = "{}/@search?UID={}&fullobjects=1".format(DIRECTORY_URL, uids)
        current_lang = api.portal.get_current_language()[:2]
        if current_lang != "fr":
            url = f"{url}&translated_in_{current_lang}=1"
        self.json_data = {
            "@id": url,
            "items": results_items,
            "items_total": len(results_items),
        }
        self.refresh_modification_date()
        return batch_results(results_items, self.context.nb_contact_by_line)

    def get_contact_properties(self, json_dict):
        return ContactProperties(json_dict, self.context)
