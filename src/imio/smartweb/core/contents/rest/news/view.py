# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.rest.view import BaseRestView
from imio.smartweb.core.interfaces import IOgpViewUtils
from plone import api
from zope.interface import implementer


@implementer(IOgpViewUtils)
class NewsViewView(BaseRestView):
    """NewsView view"""

    @property
    def propose_url(self):
        return api.portal.get_registry_record("smartweb.propose_news_url")

    @property
    def display_newsfolders_titles(self):
        return self.context.display_newsfolders_titles

    @property
    def show_categories_or_topics(self):
        return self.context.show_categories_or_topics
