# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.views import CarouselOrTableSectionView
from imio.smartweb.core.contents.sections.views import HashableJsonSectionView
from imio.smartweb.core.utils import batch_results
from imio.smartweb.core.utils import get_iadeliberation_institution_from_registry
from imio.smartweb.core.utils import get_iadeliberation_json
from imio.smartweb.core.utils import hash_md5
from imio.smartweb.core.utils import remove_cache_key


class TimestampedPublicationsView(CarouselOrTableSectionView, HashableJsonSectionView):
    """TimestampedPublications Section view"""

    @property
    def items(self):
        iadeliberation_institution = get_iadeliberation_institution_from_registry()
        max_items = self.context.nb_results_by_batch * self.context.max_nb_batches
        selected_item = "&UID=".join(self.context.related_timestamped_publications)
        modified_hash = hash_md5(str(self.context.modification_date))
        params = [
            selected_item,
            "portal_type=Publication",
            "fullobjects=y",
            "metadata_fields=UID",
            "metadata_fields=id",
            "review_state=published",
            "sort_on=sortable_title",
            "metadata_fields=modified",
            "metadata_fields=effective",
            f"cache_key={modified_hash}",
            f"sort_limit={max_items}",
        ]
        url = "{}/@search?UID={}".format(iadeliberation_institution, "&".join(params))
        self.json_data = get_iadeliberation_json(url)
        self.json_data = remove_cache_key(self.json_data)
        self.refresh_modification_date()
        if self.json_data is None or len(self.json_data.get("items", [])) == 0:
            return []
        items = self.json_data.get("items")[:max_items]
        results = []
        for item in items:
            type_document = None
            category = None
            if item.get("document_type"):
                type_document = item.get("document_type").get("title")
            if item.get("category"):
                category = item.get("category").get("title")
            dict_item = {
                "uid": item.get("UID"),
                "title": item.get("title"),
                "description": item.get("description"),
                "url": item.get("@id"),
                "effective": item.get("effective"),
                "publication_document_type": type_document,
                "publication_category": category,
                "publication_attached_file": item.get("file"),
                "has_image": False,
            }
            results.append(dict_item)
        return batch_results(results, self.context.nb_results_by_batch)

    @property
    def see_all_url(self):
        return self.context.linking_rest_view.to_object.absolute_url()
