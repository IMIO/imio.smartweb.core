# -*- coding: utf-8 -*-

from imio.smartweb.core.config import NEWS_URL
from imio.smartweb.core.contents.sections.views import CarouselOrTableSectionView
from imio.smartweb.core.utils import batch_results
from imio.smartweb.core.utils import get_json
from plone import api
from Products.CMFPlone.utils import normalizeString


class NewsView(CarouselOrTableSectionView):
    """News Section view"""

    @property
    def items(self):
        max_items = self.context.nb_results_by_batch * self.context.max_nb_batches
        selected_item = f"selected_news_folders={self.context.related_news}"
        specific_related_newsitems = self.context.specific_related_newsitems
        if specific_related_newsitems:
            selected_item = "&".join(
                [f"UID={newsitem_uid}" for newsitem_uid in specific_related_newsitems]
            )
        params = [
            selected_item,
            "portal_type=imio.news.NewsItem",
            "metadata_fields=category_title",
            "metadata_fields=has_leadimage",
            "metadata_fields=image_scales",
            "metadata_fields=effective",
            "metadata_fields=UID",
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
        url = "{}/@search?{}".format(NEWS_URL, "&".join(params))
        json_search_news = get_json(url)
        if (
            json_search_news is None
            or len(json_search_news.get("items", [])) == 0  # NOQA
        ):
            return []
        linking_view_url = self.context.linking_rest_view.to_object.absolute_url()
        image_scale = self.image_scale
        items = json_search_news.get("items")[:max_items]
        results = []
        for item in items:
            item_id = normalizeString(item["title"])
            item_url = item["@id"]
            item_uid = item["UID"]
            image_url = ""
            dict_item = {
                "uid": item_uid,
                "title": item["title"],
                "description": item["description"],
                "category": item["category_title"],
                "effective": item["effective"],
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
        if specific_related_newsitems:
            results = sorted(
                results, key=lambda x: specific_related_newsitems.index(x["uid"])
            )
        return batch_results(results, self.context.nb_results_by_batch)

    @property
    def see_all_url(self):
        return self.context.linking_rest_view.to_object.absolute_url()
