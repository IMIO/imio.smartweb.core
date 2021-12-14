# -*- coding: utf-8 -*-

from datetime import date
from dateutil.parser import parse
from imio.smartweb.core.config import EVENTS_URL
from imio.smartweb.core.contents.sections.views import CarouselOrTableSectionView
from imio.smartweb.core.utils import batch_results
from imio.smartweb.core.utils import get_json
from imio.smartweb.locales import SmartwebMessageFactory as _
from Products.CMFPlone.utils import normalizeString
from zope.globalrequest import getRequest
from zope.i18n import translate


def make_date_str(start, end):
    if start and end and start.date() != end.date():
        return translate(
            _(
                "From ${start} to ${end}",
                mapping={
                    "start": start.strftime("%d/%m"),
                    "end": end.strftime("%d/%m"),
                },
            ),
            context=getRequest(),
        )

    return translate(
        _("On ${start}", mapping={"start": start.strftime("%d/%m")}),
        context=getRequest(),
    )


class EventsView(CarouselOrTableSectionView):
    """Events Section view"""

    @property
    def items(self):
        start = date.today().isoformat()
        max_items = self.context.nb_results_by_batch * self.context.max_nb_batches
        selected_item = f"selected_agendas={self.context.related_events}"
        specific_related_events = self.context.specific_related_events
        if specific_related_events is not None:
            for event_uid in specific_related_events:
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
            start = item["start"] and parse(item["start"]) or None
            end = item["end"] and parse(item["end"]) or None
            date_str = make_date_str(start, end)
            results.append(
                {
                    "title": item["title"],
                    "description": item["description"],
                    "category": item["category_title"],
                    "event_date": date_str,
                    "url": f"{linking_view_url}#/{item_id}?u={item_uid}",
                    "image": f"{item_url}/@@images/image/{image_scale}",
                    "has_image": item["has_leadimage"],
                }
            )
        return batch_results(results, self.context.nb_results_by_batch)

    @property
    def see_all_url(self):
        return self.context.linking_rest_view.to_object.absolute_url()
