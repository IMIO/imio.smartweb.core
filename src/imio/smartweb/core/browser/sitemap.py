from BTrees.OOBTree import OOBTree
from imio.smartweb.core.config import DIRECTORY_URL
from imio.smartweb.core.config import EVENTS_URL
from imio.smartweb.core.config import NEWS_URL
from imio.smartweb.core.utils import get_json
from plone import api
from plone.base.interfaces import IPloneSiteRoot
from plone.app.layout.sitemap.sitemap import SiteMapView
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import normalizeString
from zope.component import getUtility


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

        auth_sources = [
            {"directory": {"path": DIRECTORY_URL, "type": "imio.directory.Contact"}},
            {"news": {"path": NEWS_URL, "type": "imio.news.NewsItem"}},
            {"events": {"path": EVENTS_URL, "type": "imio.events.Event"}},
        ]
        for auth_source in auth_sources:
            for auth_source_key, auth_source_value in auth_source.items():
                entity_uid = api.portal.get_registry_record(
                    f"smartweb.{auth_source_key}_entity_uid", default=None
                )
                auth_source_uid = api.portal.get_registry_record(
                    f"smartweb.default_{auth_source_key}_view", default=None
                )
                if entity_uid is None or auth_source_uid is None:
                    continue
                brains = api.content.find(UID=auth_source_uid)
                obj = brains[0].getObject()
                auth_source_view_url = obj.absolute_url()
                endpoint = "@search"
                if auth_source_key == "directory":
                    selected_container = f"selected_entities={entity_uid}"
                if auth_source_key == "news":
                    selected_container = (
                        f"selected_news_folders={obj.selected_news_folder}"
                    )
                if auth_source_key == "events":
                    selected_container = f"selected_agendas={obj.selected_agenda}"
                    endpoint = "@events"
                params = [
                    selected_container,
                    f"portal_type={auth_source_value.get('type')}",
                    "fullobjects=0",
                    "sort_on=sortable_title",
                ]
                url = f"{auth_source_value.get('path')}/{endpoint}?{'&'.join(params)}"
                results = get_json(url)
                if results is None:
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
