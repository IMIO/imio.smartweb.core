# -*- coding: utf-8 -*-

from datetime import datetime
from imio.smartweb.core.config import EVENTS_URL
from imio.smartweb.core.contents.sections.views import SectionView
from imio.smartweb.core.utils import get_json


class EventsView(SectionView):
    """Events Section view"""

    @property
    def items(self):
        number_of_items_in_batch = self.context.nb_results_by_batch
        now = datetime.now()
        start = now.strftime("%Y-%m-%d, %H:%M:%S")
        params = [
            f"selected_agendas={self.context.related_events}",
            "portal_type=imio.events.Event",
            "metadata_fields=category",
            "metadata_fields=start",
            "metadata_fields=end",
            "metadata_fields=effective",
            "metadata_fields=getIcon",
            f"limit={self.context.max_nb_results}",
            f"start.query={start}",
            "start.range=min",
        ]

        url = "{}/@search?{}".format(EVENTS_URL, "&".join(params))
        json_search_events = get_json(url)
        if (
            json_search_events is None
            or len(json_search_events.get("items", [])) == 0  # NOQA
        ):
            return
        lst_dict = []
        batch = []
        list_items = json_search_events.get("items")[: self.context.max_nb_results]
        list_size = len(list_items)
        for cpt, item in enumerate(list_items, start=1):
            url = item["@id"]
            dict = {
                "title": item["title"],
                "description": item["description"],
                "url": url,
                "image": f"{url}/@@images/image/{getattr(self.context, 'image_scale', '')}",
                "has_image": item["getIcon"],
            }
            batch.append(dict)
            if (
                cpt % number_of_items_in_batch == 0
                or list_size < number_of_items_in_batch  # noqa
            ) and cpt > 0:
                lst_dict.append(batch)
                batch = []
        if batch != []:
            lst_dict.append(batch)
        return lst_dict

    def lead_image(self, events):
        if events is None:
            return
        events_url = events["@id"]
        return "{}/{}".format(events_url, "@@images/image/")
