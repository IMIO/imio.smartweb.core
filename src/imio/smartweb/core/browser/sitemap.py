from BTrees.OOBTree import OOBTree
from imio.smartweb.core.config import DIRECTORY_URL
from imio.smartweb.core.config import EVENTS_URL
from imio.smartweb.core.config import NEWS_URL
from imio.smartweb.core.contents.rest.utils import get_auth_sources_response
from imio.smartweb.core.contents.rest.utils import get_entity_id
from plone import api
from plone.base.interfaces import IPloneSiteRoot
from plone.app.layout.sitemap.sitemap import SiteMapView
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import normalizeString
from zope.component import getUtility

import logging

logger = logging.getLogger("imio.smartweb.core")


class CustomSiteMapView(SiteMapView):

    def objects(self):
        """Returns the data to create the sitemap."""

        friendlytypes = [
            "Link",
            "imio.smartweb.Folder",
            "LIF",
            "LRF",
            "imio.smartweb.Page",
            "imio.smartweb.Procedure",
            "File",
            "Collection",
            "imio.smartweb.PortalPage",
            "Image",
            "imio.smartweb.CirkwiView",
        ]

        catalog = getToolByName(self.context, "portal_catalog")
        query = {}
        utils = getToolByName(self.context, "plone_utils")
        query["portal_type"] = utils.getUserFriendlyTypes(friendlytypes)
        registry = getUtility(IRegistry)
        typesUseViewActionInListings = frozenset(
            registry.get("plone.types_use_view_action_in_listings", [])
        )

        is_plone_site_root = IPloneSiteRoot.providedBy(self.context)
        if not is_plone_site_root:
            query["path"] = "/".join(self.context.getPhysicalPath())

        query["is_default_page"] = True
        default_page_modified = OOBTree()
        for item in catalog.searchResults(query):
            key = item.getURL().rsplit("/", 1)[0]
            value = (item.modified.micros(), item.modified.ISO8601())
            default_page_modified[key] = value

        # The plone site root is not catalogued.
        if is_plone_site_root:
            loc = self.context.absolute_url()
            date = self.context.modified()
            # Comparison must be on GMT value
            modified = (date.micros(), date.ISO8601())
            default_modified = default_page_modified.get(loc, None)
            if default_modified is not None:
                modified = max(modified, default_modified)
            lastmod = modified[1]
            yield {
                "loc": loc,
                "lastmod": lastmod,
                # 'changefreq': 'always',
                #  hourly/daily/weekly/monthly/yearly/never
                # 'prioriy': 0.5, # 0.0 to 1.0
            }

        query["is_default_page"] = False
        for item in catalog.searchResults(query):
            loc = item.getURL()
            date = item.modified
            # Comparison must be on GMT value
            modified = (date.micros(), date.ISO8601())
            default_modified = default_page_modified.get(loc, None)
            if default_modified is not None:
                modified = max(modified, default_modified)
            lastmod = modified[1]
            if item.portal_type in typesUseViewActionInListings:
                loc += "/view"
            yield {
                "loc": loc,
                "lastmod": lastmod,
            }

        auth_sources = {
            "directory": {
                "entity_reg_var": "smartweb.directory_entity_uid",
                "main_rest_view": "smartweb.default_directory_view",
                "vocabulary": "imio.smartweb.vocabulary.RemoteDirectoryEntities",
                "url": DIRECTORY_URL,
            },
            "events": {
                "entity_reg_var": "smartweb.events_entity_uid",
                "main_rest_view": "smartweb.default_events_view",
                "vocabulary": "imio.smartweb.vocabulary.RemoteEventsEntities",
                "url": EVENTS_URL,
            },
            "news": {
                "entity_reg_var": "smartweb.news_entity_uid",
                "main_rest_view": "smartweb.default_news_view",
                "vocabulary": "imio.smartweb.vocabulary.RemoteNewsEntities",
                "url": NEWS_URL,
            },
        }
        for auth_source_key, auth_source_value in auth_sources.items():
            entity_uid = api.portal.get_registry_record(
                auth_source_value.get("entity_reg_var")
            )
            if entity_uid is None:
                return self.request.response.setStatus(404, "No entity found")
            entity_id = get_entity_id(auth_source_value.get("vocabulary"), entity_uid)
            auth_source_uid = api.portal.get_registry_record(
                f"smartweb.default_{auth_source_key}_view", default=None
            )
            if auth_source_uid is None:
                return self.request.response.setStatus(
                    404, "No default authentic source found"
                )
            obj = api.content.get(UID=auth_source_uid)
            if obj is None:
                logger.warning(
                    f"Seems that a main authentic view (for {auth_source_key}) is not found"
                )
                continue
            auth_source_view_url = obj.absolute_url()
            results = get_auth_sources_response(
                auth_source_key, normalizeString(entity_id), (60 * 60 * 24)
            ).json()
            if results is None or results.get("type") == "ValueError":
                continue
            for item in results.get("items"):
                item_id = normalizeString(item.get("title"))
                item_uid = item.get("id")
                loc = f"{auth_source_view_url}/{item_id}?u={item_uid}"
                lastmod = item.get("modified")
                yield {
                    "loc": loc,
                    "lastmod": lastmod,
                }
