# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.contact.utils import ContactProperties
from imio.smartweb.core.contents.sections.views import HashableJsonSectionView
from imio.smartweb.core.utils import batch_results
from zope.component import queryMultiAdapter


class ContactView(HashableJsonSectionView):
    """Contact Section view"""

    def contacts(self):
        # Firstly, try to get contact from the container view
        container_view = queryMultiAdapter(
            (self.context.aq_parent, self.request), name="full_view"
        )
        self.json_data = container_view.get_page_contacts()
        if self.json_data is None or len(self.json_data.get("items", [])) == 0:
            return []

        container_contacts = self.json_data.get("items")
        results = [
            contact
            for contact in container_contacts
            if contact["UID"] in self.context.related_contacts
        ]
        index_map = {
            value: index for index, value in enumerate(self.context.related_contacts)
        }
        results = sorted(results, key=lambda x: index_map[x["UID"]])
        # TODO there is for sure a better way than storing json_data that
        # is not really JSON
        self.json_data = results
        self.refresh_modification_date()
        return batch_results(results, self.context.nb_contact_by_line)

    def get_contact_properties(self, json_dict):
        return ContactProperties(json_dict, self.context)
