# -*- coding: utf-8 -*-

from datetime import date
from imio.smartweb.core.config import EVENTS_URL
from imio.smartweb.core.contents.sections.views import CarouselOrTableSectionView
from imio.smartweb.core.utils import batch_results
from imio.smartweb.core.utils import get_json
from Products.CMFPlone.utils import normalizeString


class EventsView(CarouselOrTableSectionView):
    """Events Section view"""

    @property
    def items(self):
        start = date.today().isoformat()
        max_items = self.context.nb_results_by_batch * self.context.max_nb_batches
        params = [
            f"selected_agendas={self.context.related_events}",
            "portal_type=imio.events.Event",
            "metadata_fields=category",
            "metadata_fields=topics",
            "metadata_fields=start",
            "metadata_fields=end",
            "metadata_fields=has_leadimage",
            "metadata_fields=UID",
            f"start.query={start}",
            "start.range=min",
            "sort_on=start",
            f"sort_limit={max_items}",
        ]

        url = "{}/@search?{}".format(EVENTS_URL, "&".join(params))
        json_search_events = get_json(url)
        if (
            json_search_events is None
            or len(json_search_events.get("items", [])) == 0  # NOQA
        ):
            return []
        linking_view_url = self.context.linking_rest_view.to_object.absolute_url()
        image_scale = self.image_scale
        items = json_search_events.get("items")[:max_items]
        results = []
        for item in items:
            item_id = normalizeString(item["title"])
            item_url = item["@id"]
            item_uid = item["UID"]
            results.append(
                {
                    "title": item["title"],
                    "description": item["description"],
                    "url": f"{linking_view_url}/{item_id}?u={item_uid}",
                    "image": f"{item_url}/@@images/image/{image_scale}",
                    "has_image": item["has_leadimage"],
                }
            )
        return batch_results(results, self.context.nb_results_by_batch)

    @property
    def see_all_url(self):
        return self.context.linking_rest_view.to_object.absolute_url()
