# -*- coding: utf-8 -*-

from datetime import date
from dateutil.parser import parse
from imio.smartweb.common.utils import translate_vocabulary_term
from imio.smartweb.core.config import EVENTS_URL
from imio.smartweb.core.contents.rest.search.endpoint import get_default_view_url
from imio.smartweb.core.contents.sections.views import CarouselOrTableSectionView
from imio.smartweb.core.contents.sections.views import HashableJsonSectionView
from imio.smartweb.core.utils import batch_results

# TODO ?
# from imio.smartweb.core.utils import get_events_auth_header
from imio.smartweb.core.utils import get_json
from imio.smartweb.core.utils import hash_md5
from imio.smartweb.core.utils import remove_cache_key
from plone import api
from Products.CMFPlone.utils import normalizeString
from pytz import timezone

BRUSSELS_TZ = timezone("Europe/Brussels")


class EventsView(CarouselOrTableSectionView, HashableJsonSectionView):
    """Events Section view"""

    @property
    def items(self):
        today = date.today().isoformat()
        max_items = self.context.nb_results_by_batch * self.context.max_nb_batches
        specific_related_events = self.context.specific_related_events
        use_selection = self.use_selection
        if use_selection:
            selected_item = "&".join(
                [f"UID={event_uid}" for event_uid in specific_related_events]
            )
        else:
            selected_item = f"selected_agendas={self.context.related_events}"
        modified_hash = hash_md5(str(self.context.modification_date))
        params = [
            selected_item,
            "metadata_fields=container_uid",
            "metadata_fields=category_title",
            "metadata_fields=local_category",
            "metadata_fields=topics",
            "metadata_fields=start",
            "metadata_fields=end",
            "metadata_fields=has_leadimage",
            "metadata_fields=modified",
            "metadata_fields=UID",
            # review_state=published => by default, @events endpoint has this filter.
            f"cache_key={modified_hash}",
            f"event_dates.query={today}",
            "event_dates.range=min",
            f"b_size={max_items}",
        ]
        current_lang = api.portal.get_current_language()[:2]
        if current_lang != "fr":
            params.append("translated_in_{}=1".format(current_lang))
        if not use_selection:
            params += [
                "sort_on=event_dates",
            ]
        url = "{}/@events?{}".format(EVENTS_URL, "&".join(params))
        self.json_data = get_json(url, timeout=15)
        # TODO ?
        # self.json_data = get_json(url, auth=get_events_auth_header(), timeout=15)
        self.json_data = remove_cache_key(self.json_data)
        self.refresh_modification_date()
        if self.json_data is None or len(self.json_data.get("items", [])) == 0:
            return []
        linking_view_url = self.item_view_url
        image_scale = self.image_scale
        orientation = self.context.orientation
        items = self.json_data.get("items")[:max_items]
        results = []
        for item in items:
            item_id = normalizeString(item["title"])
            item_url = item["@id"]
            item_uid = item["UID"]
            # whole_day et tous les événements sont stockés/servis en UTC par
            # @events. Pour l'affichage (macros.pt utilise strftime('%d')), on
            # convertit en TZ locale Bruxelles afin que le jour calendaire soit
            # celui vu par l'utilisateur.
            start = (
                item["start"] and parse(item["start"]).astimezone(BRUSSELS_TZ) or None
            )
            end = item["end"] and parse(item["end"]).astimezone(BRUSSELS_TZ) or None
            date_dict = {"start": start, "end": end}
            modified_hash = hash_md5(item["modified"])
            category = ""
            if self.context.show_categories_or_topics == "category":
                if "local_category" in item and item.get("local_category") is not None:
                    local_category = item.get("local_category")
                    category = (
                        local_category
                        if isinstance(local_category, str)
                        else local_category.get("title", "")
                    )
                else:
                    category = item.get("category_title", "")
            elif self.context.show_categories_or_topics == "topic":
                topic = item.get("topics") and item["topics"][0] or None
                category = translate_vocabulary_term(
                    "imio.smartweb.vocabulary.Topics", topic
                )
            dict_item = {
                "uid": item_uid,
                "title": item["title"],
                "description": item["description"],
                "category": category,
                "event_date": date_dict,
                "url": f"{linking_view_url}/{item_id}?u={item_uid}",
                "container_id": item.get("usefull_container_id", None),
                "container_title": item.get("usefull_container_title", None),
                "has_image": item["has_leadimage"],
                "image": f"{item_url}/@@images/image/{orientation}_{image_scale}?cache_key={modified_hash}",
            }
            results.append(dict_item)
        if use_selection:
            results = sorted(
                results, key=lambda x: specific_related_events.index(x["uid"])
            )
        return batch_results(results, self.context.nb_results_by_batch)

    @property
    def use_selection(self):
        """Whether this section lists hand-picked items rather than an agenda.

        ``events_source`` is what decides, not the mere presence of values in
        ``specific_related_events``: both fields keep their value when the
        editor switches source, so switching back must restore the agenda.
        """
        return self.context.events_source == "selection" and bool(
            self.context.specific_related_events
        )

    @property
    def linking_view_url(self):
        """The view this section's agenda belongs to, "" when unset.

        ``linking_rest_view`` is optional now (a hand-picked section has no use
        for one), so it can legitimately be None.
        """
        rest_view = getattr(self.context.linking_rest_view, "to_object", None)
        return rest_view is not None and rest_view.absolute_url() or ""

    @property
    def item_view_url(self):
        """Where the items of this section link to.

        A hand-picked event comes from anywhere in the entity, so
        ``linking_rest_view`` plays no part: it links to the site's default
        events view, and ``BaseEventsEndpoint`` retries an unscoped lookup by
        UID so the detail page resolves even when that view shows another
        agenda, another event type or another date range. The invariant refuses
        to save such a section while the control panel has no default events
        view, so "" here means it was emptied after.
        """
        if self.use_selection:
            return get_default_view_url("events")
        return self.linking_view_url

    @property
    def see_all_url(self):
        # a hand-picked section has no linking view: its "see all" belongs to
        # the same default view its items link to
        return self.item_view_url

    def is_multi_dates(self, start, end):
        return start and end and start.date() != end.date()

    @property
    def display_container_title(self):
        return self.context.display_agendas_titles
