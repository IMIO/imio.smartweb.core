from Acquisition import aq_inner
from BTrees.OOBTree import OOBTree
from imio.smartweb.core.config import DIRECTORY_URL
from imio.smartweb.core.config import EVENTS_URL
from imio.smartweb.core.config import NEWS_URL
from imio.smartweb.core.contents.rest.directory.endpoint import DirectoryEndpointGet
from imio.smartweb.core.contents.rest.events.endpoint import EventsEndpointGet
from imio.smartweb.core.contents.rest.news.endpoint import NewsEndpointGet
from imio.smartweb.core.interfaces import IImioSmartwebCoreLayer
from plone.app.layout.navigation.navtree import buildFolderTree
from plone.app.layout.sitemap.sitemap import SiteMapView
from plone.base.interfaces import IPloneSiteRoot
from Products.CMFPlone.browser.navigation import CatalogSiteMap as BaseCatalogSiteMap
from Products.CMFPlone.browser.navtree import (
    SitemapNavtreeStrategy as BaseSitemapNavtreeStrategy,
)
from Products.CMFPlone.browser.navtree import (
    SitemapQueryBuilder as BaseSitemapQueryBuilder,
)
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import normalizeString
from zope.component import getMultiAdapter
from zope.interface import implementer
from zope.interface import Interface

import logging
import Missing

logger = logging.getLogger("imio.smartweb.core")


FRIENDLY_TYPES = [
    "Collection",
    "Image",
    "Link",
    "imio.smartweb.Folder",
    "imio.smartweb.Page",
    "imio.smartweb.PortalPage",
    "imio.smartweb.Procedure",
    "imio.smartweb.CirkwiView",
    "imio.smartweb.DirectoryView",
    "imio.smartweb.EventsView",
    "imio.smartweb.NewsView",
]


def get_endpoint_data(obj, request):
    """Retourne les données issues du bon endpoint pour un objet donné"""
    endpoint_mapping = {
        "imio.smartweb.DirectoryView": DirectoryEndpointGet,
        "imio.smartweb.EventsView": EventsEndpointGet,
        "imio.smartweb.NewsView": NewsEndpointGet,
    }

    endpoint_class = endpoint_mapping.get(obj.portal_type)
    if not endpoint_class:
        return {}

    endpoint = endpoint_class()
    batch_size = 1000 if obj.portal_type == "imio.smartweb.DirectoryView" else 365
    return (
        endpoint.reply_for_given_object(
            obj, request, fullobjects=0, batch_size=batch_size
        )
        or {}
    )


def format_sitemap_items(items, base_url):
    """Formatte les items pour le sitemap"""
    formatted_items = []
    for item in items:
        item_id = normalizeString(item.get("title"))
        item_uid = item.get("id")
        lastmod = item.get("modified") or "1970-01-01T00:00:00Z"
        formatted_items.append(
            {
                "loc": f"{base_url}/{item_id}?u={item_uid}",
                "lastmod": lastmod,
                "Title": item_id,
                "Description": item.get("description", ""),
                "getURL": f"{base_url}/{item_id}?u={item_uid}",
                "getRemoteUrl": Missing.Value,
                "currentItem": False,
                "currentParent": False,
                "normalized_review_state": "published",
                "normalized_portal_type": "imio-smartweb-directory-item",
            }
        )
    return formatted_items


class CustomSiteMapView(SiteMapView):
    """Custom sitemap view. (get items for sitemap.xml.gz)"""

    def objects(self):
        """Returns the data to create the sitemap."""
        friendlytypes = FRIENDLY_TYPES

        catalog = getToolByName(self.context, "portal_catalog")
        query = {
            "portal_type": getToolByName(
                self.context, "plone_utils"
            ).getUserFriendlyTypes(friendlytypes)
        }

        is_plone_site_root = IPloneSiteRoot.providedBy(self.context)
        if not is_plone_site_root:
            query["path"] = "/".join(self.context.getPhysicalPath())

        query["is_default_page"] = True
        default_page_modified = OOBTree()
        for item in catalog.searchResults(query):
            key = item.getURL().rsplit("/", 1)[0]
            value = (item.modified.micros(), item.modified.ISO8601())
            default_page_modified[key] = value

        if is_plone_site_root:
            loc = self.context.absolute_url()
            date = self.context.modified()
            modified = max(
                (date.micros(), date.ISO8601()), default_page_modified.get(loc, (0, ""))
            )
            yield {"loc": loc, "lastmod": modified[1]}

        query["is_default_page"] = False
        for item in catalog.searchResults(query):
            loc = item.getURL()
            date = item.modified
            modified = max(
                (date.micros(), date.ISO8601()), default_page_modified.get(loc, (0, ""))
            )
            yield {"loc": loc, "lastmod": modified[1]}

        for brain in catalog(
            portal_type=[
                "imio.smartweb.EventsView",
                "imio.smartweb.NewsView",
                "imio.smartweb.DirectoryView",
            ]
        ):
            obj = brain.getObject()
            data = get_endpoint_data(obj, obj.REQUEST)
            yield from format_sitemap_items(data.get("items", {}), obj.absolute_url())


@implementer(IImioSmartwebCoreLayer)
class CatalogSiteMap(BaseCatalogSiteMap):
    def siteMap(self):
        context = aq_inner(self.context)

        queryBuilder = SitemapQueryBuilder(context)
        query = queryBuilder()
        strategy = getMultiAdapter((context, self), ISmartwebNavtreeStrategy)
        base_folder_tree = buildFolderTree(
            context, obj=context, query=query, strategy=strategy
        )

        for child in base_folder_tree.get("children"):
            obj = child.get("item").getObject()
            data = get_endpoint_data(obj, obj.REQUEST)
            if not data:
                continue
            child["children"] = format_sitemap_items(
                data.get("items", []), obj.absolute_url()
            )

        return base_folder_tree


class SitemapQueryBuilder(BaseSitemapQueryBuilder):
    """Construit la requête pour le sitemap avec des types de contenu personnalisés."""

    def __init__(self, context):
        self.context = context

    def __call__(self):
        query = {}
        custom_query = getattr(self.context, "getCustomNavQuery", None)
        if custom_query and callable(custom_query):
            query = custom_query()
        query["portal_type"] = FRIENDLY_TYPES
        query["review_state"] = "published"
        return query


class ISmartwebNavtreeStrategy(Interface):
    """Marker interface for the smartweb navtree strategy."""


@implementer(ISmartwebNavtreeStrategy)
class SitemapNavtreeStrategy(BaseSitemapNavtreeStrategy):

    def nodeFilter(self, node):
        # Return all nodes in sitemap even if they are exclude from nav
        return True
