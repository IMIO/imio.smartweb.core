# -*- coding: utf-8 -*-

from imio.smartweb.core.config import DIRECTORY_URL
from imio.smartweb.core.contents.sections.contact.utils import ContactProperties
from imio.smartweb.core.contents.sections.views import HashableJsonSectionView
from imio.smartweb.core.utils import batch_results
from imio.smartweb.core.utils import get_json
from plone import api
from zope.component import queryMultiAdapter

import time


# class ContactView(HashableJsonSectionView):
#     """Contact Section view"""

#     def contacts(self):
#         start_time = time.time()
#         if self.context.related_contacts is None:
#             return
#         related_contacts = self.context.related_contacts
#         uids = "&UID=".join(related_contacts)
#         url = "{}/@search?UID={}&fullobjects=1".format(DIRECTORY_URL, uids)
#         current_lang = api.portal.get_current_language()[:2]
#         if current_lang != "fr":
#             url = f"{url}&translated_in_{current_lang}=1"
#         self.json_data = get_json(url)
#         self.refresh_modification_date()
#         if self.json_data is None or len(self.json_data.get("items", [])) == 0:  # NOQA
#             return
#         results = self.json_data.get("items")
#         index_map = {value: index for index, value in enumerate(related_contacts)}
#         results = sorted(results, key=lambda x: index_map[x["UID"]])
#         end_time = time.time()
#         execution_time = end_time - start_time
#         print(f"Temps d'exécution: {execution_time:.4f} secondes")

#         return batch_results(results, self.context.nb_contact_by_line)

#     def get_contact_properties(self, json_dict):
#         return ContactProperties(json_dict, self.context)


class ContactView(HashableJsonSectionView):
    """Contact Section view"""

    def contacts(self):
        # Firstly, try to get contact from the container view
        container_view = queryMultiAdapter(
            (self.context.aq_parent, self.request), name="full_view"
        )
        import pdb

        pdb.set_trace()
        self.refresh_modification_date()
        container_contacts = container_view.get_related_contacts()
        if container_contacts is None or container_contacts == []:
            return self.get_this_contact_from_directory()
        else:
            results = [
                contact
                for contact in container_contacts
                if contact["UID"] in self.context.related_contacts
            ]
            index_map = {
                value: index
                for index, value in enumerate(self.context.related_contacts)
            }
            results = sorted(results, key=lambda x: index_map[x["UID"]])
            return batch_results(results, self.context.nb_contact_by_line)

    def get_this_contact_from_directory(self):
        import pdb

        pdb.set_trace()
        if self.context.related_contacts is None:
            return
        related_contacts = self.context.related_contacts
        uids = "&UID=".join(related_contacts)
        url = "{}/@search?UID={}&fullobjects=1".format(DIRECTORY_URL, uids)
        current_lang = api.portal.get_current_language()[:2]
        if current_lang != "fr":
            url = f"{url}&translated_in_{current_lang}=1"
        self.json_data = get_json(url)
        self.refresh_modification_date()
        if self.json_data is None or len(self.json_data.get("items", [])) == 0:  # NOQA
            return
        results = self.json_data.get("items")
        index_map = {value: index for index, value in enumerate(related_contacts)}
        results = sorted(results, key=lambda x: index_map[x["UID"]])
        return batch_results(results, self.context.nb_contact_by_line)

    def get_contact_properties(self, json_dict):
        return ContactProperties(json_dict, self.context)


# http://localhost:8080/Plone/@search?UID=2dc381f0fb584381b8e4a19c84f53b35&fullobjects=1
