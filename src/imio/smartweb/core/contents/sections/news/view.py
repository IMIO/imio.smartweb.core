# -*- coding: utf-8 -*-

from imio.smartweb.core.config import NEWS_URL
from imio.smartweb.core.contents.sections.views import SectionWithCarouselView
from imio.smartweb.core.utils import batch_results
from imio.smartweb.core.utils import get_json
from Products.CMFPlone.utils import normalizeString


class NewsView(SectionWithCarouselView):
    """News Section view"""

    @property
    def items(self):
        params = [
            f"selected_news_folders={self.context.related_news}",
            "portal_type=imio.news.NewsItem",
            "metadata_fields=category",
            "metadata_fields=topics",
            "metadata_fields=has_leadimage",
            "metadata_fields=UID",
            "sort_on=effective",
            "sort_order=descending",
            f"sort_limit={self.context.max_nb_results}",
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
        items = json_search_news.get("items")[: self.context.max_nb_results]
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
