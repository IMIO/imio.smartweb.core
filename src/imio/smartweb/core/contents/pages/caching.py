# -*- coding: utf-8 -*-

from dateutil.parser import parse
from imio.smartweb.core.config import NEWS_URL
from imio.smartweb.core.contents import IPages
from imio.smartweb.core.contents.sections.news.content import ISectionNews
from imio.smartweb.core.utils import get_json
from plone import api
from plone.app.caching.lastmodified import CatalogableDublinCoreLastModified
from plone.memoize import ram
from time import time
from z3c.caching.interfaces import ILastModified
from zope.component import adapter
from zope.interface import implementer


@ram.cache(lambda func, url: (url, time() // 60))
def _latest_news_modification(url):
    json_data = get_json(url, timeout=2)
    if not json_data or not json_data.get("items"):
        return None
    modified = json_data["items"][0].get("modified")
    return modified and parse(modified) or None


def latest_news_modification(section):
    """Modification date of the latest news that the section can display"""
    if section.specific_related_newsitems:
        selected_item = "&".join(
            [f"UID={uid}" for uid in section.specific_related_newsitems]
        )
    elif section.related_news:
        selected_item = f"selected_news_folders={section.related_news}"
    else:
        return None
    entity_uid = api.portal.get_registry_record("smartweb.news_entity_uid")
    params = [
        selected_item,
        "portal_type=imio.news.NewsItem",
        "review_state=published",
        "metadata_fields=modified",
        f"entity_uid={entity_uid}",
        "sort_on=modified",
        "sort_order=descending",
        "sort_limit=1",
    ]
    url = "{}/@search_newsitems?{}".format(NEWS_URL, "&".join(params))
    return _latest_news_modification(url)


@implementer(ILastModified)
@adapter(IPages)
class PagesLastModified(CatalogableDublinCoreLastModified):
    """An anonymous rendering never changes the page modification date (no ZODB
    write), so the date of the remote news shown in the page must change the
    Last-Modified header and the ETag. Else Varnish and browsers get a 304 with
    the old news.
    """

    def __call__(self):
        dates = [super().__call__()]
        for section in self.context.objectValues():
            if ISectionNews.providedBy(section):
                dates.append(latest_news_modification(section))
        dates = [d for d in dates if d is not None]
        return dates and max(dates) or None
