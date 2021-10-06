# -*- coding: utf-8 -*-

from datetime import date, datetime
from datetime import timedelta
from imio.smartweb.core.config import NEWS_URL
from imio.smartweb.core.contents.sections.views import SectionView
from imio.smartweb.core.utils import get_json
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory

import json


class NewsView(SectionView):
    """News Section view"""

    @property
    def news(self):
        params = [
            "selected_news_folders={}".format(self.context.related_news),
            "portal_type=imio.news.NewsItem",
            "metadata_fields=category",
            "metadata_fields=effective",
        ]
        url = "{}/@search?{}".format(NEWS_URL, "&".join(params))
        json_search_news = get_json(url)
        if (
            json_search_news is None
            or len(json_search_news.get("items", [])) == 0  # NOQA
        ):
            return

        # [{'@id': 'https://news.staging.imio.be/braine-lalleud/2021/actu2',
        #   '@type': 'imio.news.NewsItem',
        #   'category': None,
        #   'description': 'Nouvelle actu 2',
        #   'review_state': 'published',
        #   'title': 'Actu2'},
        #  {
        #      '@id': 'https://news.staging.imio.be/braine-lalleud/2021/inauguration-du-nouveau-site-de-la-commune-de-braine-lalleud',
        #      '@type': 'imio.news.NewsItem',
        #      'category': 'presse',
        #      'description': '',
        #      'review_state': 'published',
        #      'title': "Inauguration du nouveau site de la commune de Braine l'Alleud"}]
        return json_search_news.get("items")

    def lead_image(self, news):
        if news is None:
            return
        news_url = news["@id"]
        return "{}/{}".format(news_url,"@@images/image/")
