# -*- coding: utf-8 -*-

from imio.smartweb.core.config import NEWS_URL
from imio.smartweb.core.contents.sections.views import SectionView
from imio.smartweb.core.utils import get_json


class NewsView(SectionView):
    """News Section view"""

    @property
    def items(self):
        params = [
            "selected_news_folders={}".format(self.context.related_news),
            "portal_type=imio.news.NewsItem",
            "metadata_fields=category",
            "metadata_fields=effective",
            "metadata_fields=getIcon",
        ]
        url = "{}/@search?{}".format(NEWS_URL, "&".join(params))
        json_search_news = get_json(url)
        if (
            json_search_news is None
            or len(json_search_news.get("items", [])) == 0  # NOQA
        ):
            return
        lst_dict = []

        for item in json_search_news.get("items"):
            url = item["@id"]
            dict = {
                "title": item["title"],
                "description": item["description"],
                "url": url,
                "image": f"{url}/@@images/image/{getattr(self.context, 'image_scale', '')}",
                "has_image": item["getIcon"],
            }
            lst_dict.append(dict)
        return lst_dict
