# -*- coding: utf-8 -*-

from imio.smartweb.core import config
from imio.smartweb.core.utils import get_json
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from plone.app.contentmenu.menu import BrowserMenu
from plone.app.contentmenu.menu import BrowserSubMenuItem
from plone.memoize import ram
from time import time
from zope.browsermenu.interfaces import IBrowserMenu
from zope.interface import implementer

import re


@implementer(IBrowserMenu)
class AuthenticSourcesMenuItem(BrowserSubMenuItem):

    title = _("Authentic sources")
    submenuId = "authentic-sources-menu"
    icon = "boxes"
    extra = {
        "id": "plone-authentic-sources-menu",
        "li_class": "plonetoolbar-authentic-sources-menu",
    }

    order = 50

    @property
    def action(self):
        return "#"

    def available(self):
        permission = "cmf.ModifyPortalContent"
        if api.user.has_permission(permission, obj=self.context) is False:
            return False
        news_entity_url = api.portal.get_registry_record(
            "smartweb.news_entity_uid", default=None
        )
        events_entity_url = api.portal.get_registry_record(
            "smartweb.events_entity_uid", default=None
        )
        directory_entity_url = api.portal.get_registry_record(
            "smartweb.directory_entity_uid", default=None
        )
        return news_entity_url or events_entity_url or directory_entity_url

    def selected(self):
        return False


@implementer(IBrowserMenu)
class AuthenticSourcesMenu(BrowserMenu):
    @ram.cache(lambda *args: time() // (60 * 60))
    def getMenuItems(self, context, request):
        news_entity_url = self.get_entity_from_authentic_source(
            config.NEWS_URL, "smartweb.news_entity_uid"
        )
        events_entity_url = self.get_entity_from_authentic_source(
            config.EVENTS_URL, "smartweb.events_entity_uid"
        )
        directory_entity_url = self.get_entity_from_authentic_source(
            config.DIRECTORY_URL, "smartweb.directory_entity_uid"
        )
        news = {"url": news_entity_url, "icon": "newspaper"}
        events = {"url": events_entity_url, "icon": "calendar-event"}
        directory = {"url": directory_entity_url, "icon": "file-person"}
        authentic_sources = [news, events, directory]

        menu_items = []
        for source in authentic_sources:
            if source.get("url") is None:
                continue
            title = re.compile(r"https?://(www\.)?")
            title = title.sub("", source["url"]).strip().strip("/")
            menu_item = {
                "title": title,
                "description": "",
                "action": source["url"],
                "selected": False,
                "icon": source["icon"],
                "extra": {"id": "some-id", "separator": None, "class": ""},
                "submenu": None,
            }
            menu_items.append(menu_item)
        return menu_items

    def get_entity_from_authentic_source(self, authentic_sources_url, registry_key):
        value = api.portal.get_registry_record(registry_key)
        if value is None:
            return None
        result = get_json(f"{authentic_sources_url}/@search?UID={value}")
        if not result or not result.get("items"):
            return None
        return result.get("items")[0].get("@id")
