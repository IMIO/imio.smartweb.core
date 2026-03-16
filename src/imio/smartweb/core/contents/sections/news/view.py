# -*- coding: utf-8 -*-

from imio.smartweb.common.utils import translate_vocabulary_term
from imio.smartweb.core.config import NEWS_URL
from imio.smartweb.core.contents.sections.views import CarouselOrTableSectionView
from imio.smartweb.core.contents.sections.views import HashableJsonSectionView
from imio.smartweb.locales import SmartwebMessageFactory as _
from imio.smartweb.core.utils import batch_results
from imio.smartweb.core.utils import get_json
from imio.smartweb.core.utils import hash_md5
from imio.smartweb.core.utils import remove_cache_key
from plone import api
from Products.CMFPlone.utils import normalizeString
from zope.i18n import translate


class NewsView(CarouselOrTableSectionView, HashableJsonSectionView):
    """News Section view"""

    def _get_news_folders_uids_and_title_from_entity(self, entity_uid):
        url = f"{NEWS_URL}/@search_entity?UID={entity_uid}&metadata_fields=UID"
        data = get_json(url)
        entity_uid = data.get("items")[0].get("UID")
        url_to_get_news_folders = (
            f"{data.get('items')[0].get('@id')}"
            f"/@search_newsfolder_for_entity?portal_type=imio.news.NewsFolder&metadata_fields=UID&entity_uid={entity_uid}"
        )
        data = get_json(url_to_get_news_folders)
        uids = [item["UID"] for item in data["items"]]
        data = {item["UID"]: item["title"] for item in data["items"]}
        return uids, data

    @property
    def items(self):
        entity_uid = api.portal.get_registry_record("smartweb.news_entity_uid")
        max_items = self.context.nb_results_by_batch * self.context.max_nb_batches
        # Fallback if news folder is breaked (removed from auth source)
        uids, data = self._get_news_folders_uids_and_title_from_entity(entity_uid)
        selected_item = f"selected_news_folders={self.context.related_news}"
        if self.context.related_news not in uids:
            item = next(
                (k for k, v in data.items() if "administration" in v.lower()),
                uids[0] if uids else None,
            )
            selected_item = f"selected_news_folders={item}" if item else ""
            current_lang = api.portal.get_current_language()[:2]
            self._issue = translate(
                _(
                    "Warning: Deleted news folder. We get random news folder for this section"
                ),
                target_language=current_lang,
            )
        specific_related_newsitems = self.context.specific_related_newsitems
        if specific_related_newsitems:
            selected_item = "&".join(
                [f"UID={newsitem_uid}" for newsitem_uid in specific_related_newsitems]
            )
        modified_hash = hash_md5(str(self.context.modification_date))
        params = [
            selected_item,
            "portal_type=imio.news.NewsItem",
            "review_state=published",
            "metadata_fields=container_uid",
            "metadata_fields=category_title",
            "metadata_fields=local_category",
            "metadata_fields=topics",
            "metadata_fields=has_leadimage",
            "metadata_fields=modified",
            "metadata_fields=effective",
            "metadata_fields=UID",
            f"entity_uid={entity_uid}",
            f"cache_key={modified_hash}",
            f"sort_limit={max_items}",
        ]
        current_lang = api.portal.get_current_language()[:2]
        if current_lang != "fr":
            params.append("translated_in_{}=1".format(current_lang))
        if not specific_related_newsitems:
            params += [
                "sort_on=effective",
                "sort_order=descending",
            ]
        url = "{}/@search_newsitems?{}".format(NEWS_URL, "&".join(params))
        self.json_data = get_json(url)
        self.json_data = remove_cache_key(self.json_data)
        self.refresh_modification_date()
        if self.json_data is None or len(self.json_data.get("items", [])) == 0:
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
            modified_hash = hash_md5(item["modified"])
            category = ""
            if self.context.show_categories_or_topics == "category":
                category = item.get("local_category") or item.get("category_title", "")
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
                "effective": item["effective"],
                "url": f"{linking_view_url}/{item_id}?u={item_uid}",
                "container_id": item.get("usefull_container_id", None),
                "container_title": item.get("usefull_container_title", None),
                "has_image": item["has_leadimage"],
                "image": f"{item_url}/@@images/image/{orientation}_{image_scale}?cache_key={modified_hash}",
            }
            results.append(dict_item)
        if specific_related_newsitems:
            results = sorted(
                results, key=lambda x: specific_related_newsitems.index(x["uid"])
            )
        return batch_results(results, self.context.nb_results_by_batch)

    @property
    def issue(self):
        return self._issue

    @property
    def see_all_url(self):
        return self.context.linking_rest_view.to_object.absolute_url()

    @property
    def display_container_title(self):
        return self.context.display_newsfolders_titles
