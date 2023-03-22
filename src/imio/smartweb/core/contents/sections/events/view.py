# -*- coding: utf-8 -*-

from datetime import date
from dateutil.parser import parse
from imio.smartweb.core.config import EVENTS_URL
from imio.smartweb.core.contents.sections.views import CarouselOrTableSectionView
from imio.smartweb.core.utils import batch_results
from imio.smartweb.core.utils import expand_occurences
from imio.smartweb.core.utils import get_json
from imio.smartweb.core.utils import get_start_date
from plone import api
from Products.CMFPlone.utils import normalizeString


class EventsView(CarouselOrTableSectionView):
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
            "portal_type=imio.events.Event",
            "metadata_fields=category_title",
            "metadata_fields=start",
            "metadata_fields=end",
            "metadata_fields=has_leadimage",
            "metadata_fields=image_scales",
            "metadata_fields=UID",
            "metadata_fields=recurrence",
            "metadata_fields=whole_day",
            "metadata_fields=open_end",
            f"event_dates.query={today}",
            "event_dates.range=min",
            f"sort_limit={max_items}",
        ]
        current_lang = api.portal.get_current_language()[:2]
        if current_lang != "fr":
            params.append("translated_in_{}=1".format(current_lang))
        if not specific_related_events:
            params += [
                "sort_on=event_dates",
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
        expanded_events = expand_occurences(items)
        expanded_events_sorted = sorted(expanded_events, key=get_start_date)
        # If we have specified an event with recurrences in the list of specific events, then we only keep the 1st occurrence with a non-obsolete date
        # expanded_events_sorted is sorted by "start"
        # Note : specific_related_events will be sorted by UID.
        if specific_related_events:
            res = []
            for item in items:
                for expanded_event in expanded_events_sorted:
                    if item.get("UID") == expanded_event.get("UID"):
                        res.append(expanded_event)
                        break
            expanded_events_sorted = res
        results = []
        for item in expanded_events_sorted:
            item_id = normalizeString(item["title"])
            item_url = item["@id"]
            item_uid = item["UID"]
            start = item["start"] and parse(item["start"]) or None
            end = item["end"] and parse(item["end"]) or None
            date_dict = {"start": start, "end": end}
            image_url = ""
            dict_item = {
                "uid": item_uid,
                "title": item["title"],
                "description": item["description"],
                "category": item["category_title"],
                "event_date": date_dict,
                "url": f"{linking_view_url}#/{item_id}?u={item_uid}",
                "has_image": item["has_leadimage"],
            }
            if item["has_leadimage"]:
                scales = item["image_scales"]["image"][0]["scales"]
                if image_scale in scales:
                    image_url = f"{item_url}/{scales[image_scale]['download']}"
                else:
                    dict_item["bad_scale"] = image_scale
                    no_scale_so_download = item["image_scales"]["image"][0]["download"]
                    image_url = f"{item_url}/{no_scale_so_download}"
            dict_item["image"] = image_url
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
