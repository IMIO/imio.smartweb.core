# -*- coding: utf-8 -*-

from imio.smartweb.core.config import NEWS_URL
from imio.smartweb.core.contents.sections.views import SectionView
from imio.smartweb.core.utils import get_json


class NewsView(SectionView):
    """News Section view"""

    @property
    def items(self):
        number_of_items_in_batch = self.context.nb_results_by_batch
        params = [
            f"selected_news_folders={self.context.related_news}",
            "portal_type=imio.news.NewsItem",
            "metadata_fields=category",
            "metadata_fields=effective",
            "metadata_fields=getIcon",
            f"limit={self.context.max_nb_results}",
        ]
        url = "{}/@search?{}".format(NEWS_URL, "&".join(params))
        json_search_news = get_json(url)
        if (
            json_search_news is None
            or len(json_search_news.get("items", [])) == 0  # NOQA
        ):
            return
        lst_dict = []
        batch = []
        list_items = json_search_news.get("items")[: self.context.max_nb_results]
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
