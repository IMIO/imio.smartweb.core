# -*- coding: utf-8 -*-

from imio.smartweb.core.config import DIRECTORY_URL
from imio.smartweb.core.contents.sections.contact.utils import ContactProperties
from imio.smartweb.core.contents.sections.views import HashableJsonSectionView
from imio.smartweb.core.utils import batch_results
from imio.smartweb.core.utils import get_json
from plone import api


class ContactView(HashableJsonSectionView):
    """Contact Section view"""

    def contacts(self):
        if self.context.related_contacts is None:
            return
        uids = "&UID=".join(self.context.related_contacts)
        url = "{}/@search?UID={}&fullobjects=1".format(DIRECTORY_URL, uids)
        current_lang = api.portal.get_current_language()[:2]
        if current_lang != "fr":
            url = f"{url}&translated_in_{current_lang}=1"
        self.json_data = get_json(url)
        self.refresh_modification_date()
        if self.json_data is None or len(self.json_data.get("items", [])) == 0:  # NOQA
            return
        return batch_results(
            self.json_data.get("items"), self.context.nb_contact_by_line
        )

    def get_contact_properties(self, json_dict):
        return ContactProperties(json_dict)
