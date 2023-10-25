# -*- coding: utf-8 -*-

from datetime import date
from dateutil.parser import parse
from imio.smartweb.core.config import EVENTS_URL
from imio.smartweb.core.contents.sections.views import CarouselOrTableSectionView
from imio.smartweb.core.contents.sections.views import HashableJsonSectionView
from imio.smartweb.core.utils import batch_results
from imio.smartweb.core.utils import get_json
from imio.smartweb.core.utils import hash_md5
from plone import api
from Products.CMFPlone.utils import normalizeString


class EventsView(CarouselOrTableSectionView, HashableJsonSectionView):
    """Events Section view"""

    @property
    def items(self):
        today = date.today().isoformat()
        max_items = self.context.nb_results_by_batch * self.context.max_nb_batches
        selected_item = f"selected_agendas={self.context.related_events}"
        specific_related_events = self.context.specific_related_events
        if specific_related_events:
            selected_item = "&".join(
                [f"UID={event_uid}" for event_uid in specific_related_events]
            )
        params = [
            selected_item,
            "metadata_fields=category_title",
            "metadata_fields=start",
            "metadata_fields=end",
            "metadata_fields=has_leadimage",
            "metadata_fields=modified",
            "metadata_fields=UID",
            f"event_dates.query={today}",
            "event_dates.range=min",
            f"b_size={max_items}",
        ]
        current_lang = api.portal.get_current_language()[:2]
        if current_lang != "fr":
            params.append("translated_in_{}=1".format(current_lang))
        if not specific_related_events:
            params += [
                "sort_on=event_dates",
            ]
        url = "{}/@events?{}".format(EVENTS_URL, "&".join(params))
        self.json_data = get_json(url)
        self.refresh_modification_date()
        if self.json_data is None or len(self.json_data.get("items", [])) == 0:  # NOQA
            return []
        linking_view_url = self.context.linking_rest_view.to_object.absolute_url()
        image_scale = self.image_scale
        orientation = self.context.orientation
        items = self.json_data.get("items")[:max_items]
        results = []
        for item in items:
            item_id = normalizeString(item["title"])
            item_url = item["@id"]
            item_uid = item["UID"]
            start = item["start"] and parse(item["start"]) or None
            end = item["end"] and parse(item["end"]) or None
            date_dict = {"start": start, "end": end}
            modified_hash = hash_md5(item["modified"])
            dict_item = {
                "uid": item_uid,
                "title": item["title"],
                "description": item["description"],
                "category": item["category_title"],
                "event_date": date_dict,
                "url": f"{linking_view_url}#/{item_id}?u={item_uid}",
                "has_image": item["has_leadimage"],
                "image": f"{item_url}/@@images/image/{orientation}_{image_scale}?cache_key={modified_hash}",
            }
            results.append(dict_item)
        if specific_related_events:
            results = sorted(
                results, key=lambda x: specific_related_events.index(x["uid"])
            )
        return batch_results(results, self.context.nb_results_by_batch)

    @property
    def see_all_url(self):
        return self.context.linking_rest_view.to_object.absolute_url()

    def is_multi_dates(self, start, end):
        return start and end and start.date() != end.date()
