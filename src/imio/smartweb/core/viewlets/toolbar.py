# -*- coding: utf-8 -*-

from imio.smartweb.core import config
from imio.smartweb.core.interfaces import IImioSmartwebCoreLayer
from imio.smartweb.core.utils import get_json
from imio.smartweb.core.viewlets.interfaces import IAuthenticSourcesMenu
from imio.smartweb.core.viewlets.interfaces import IAuthenticSourcesSubMenuItem
from imio.smartweb.core.viewlets.interfaces import ISmartwebHelpMenu
from imio.smartweb.core.viewlets.interfaces import ISmartwebHelpSubMenuItem
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from plone.app.contentmenu.menu import BrowserMenu
from plone.app.contentmenu.menu import BrowserSubMenuItem
from plone.memoize import ram
from time import time
from zope.interface import implementer

import os
import re


def _cache_key(func, obj, context, request):
    return (obj.id, time() // (5 * 60))


@implementer(IAuthenticSourcesSubMenuItem)
class AuthenticSourcesMenuItem(BrowserSubMenuItem):
    title = _("Authentic sources")
    submenuId = "plone_authentic_sources_menu"
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
        if not IImioSmartwebCoreLayer.providedBy(self.request):
            return False
        permission = "Modify portal content"
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


@implementer(IAuthenticSourcesMenu)
class AuthenticSourcesMenu(BrowserMenu):
    @ram.cache(_cache_key)
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
        news = {"url": news_entity_url, "icon": "newspaper", "id": "news"}
        events = {"url": events_entity_url, "icon": "calendar-event", "id": "events"}
        directory = {
            "url": directory_entity_url,
            "icon": "file-person",
            "id": "directory",
        }
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
                "extra": {
                    "id": f'plone-authentic-sources-menu{source["id"]}',
                    "separator": None,
                    "class": "",
                },
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


@implementer(ISmartwebHelpSubMenuItem)
class SmartwebHelpMenuItem(BrowserSubMenuItem):
    title = _("Please help!")
    submenuId = "plone_smartweb_help_menu"
    icon = "info-circle"
    extra = {
        "id": "plone-smartweb-help-menu",
        "li_class": "plonetoolbar-smartweb-help-menu",
    }

    order = 50

    @property
    def action(self):
        return "#"

    def available(self):
        if not IImioSmartwebCoreLayer.providedBy(self.request):
            return False
        permission = "Modify portal content"
        return api.user.has_permission(permission, obj=self.context)


@implementer(ISmartwebHelpMenu)
class SmartwebHelpMenu(BrowserMenu):
    @ram.cache(_cache_key)
    def getMenuItems(self, context, request):
        rtfm_action = os.environ.get(
            "help_menu_rtfm", "https://docs.imio.be/iasmartweb/smartweb_v6"
        )
        support_action = os.environ.get("help_menu_support", "https://support.imio.be")
        workshop_action = os.environ.get(
            "help_menu_workshop",
            "https://my-formulaires.imio.be/ateliers-imio/ateliers-iasmartweb-1",
        )

        # Read The Funny Manual... (no?)
        rtfm = {
            "title": _("Read documentation"),
            "description": "",
            "action": rtfm_action,
            "selected": False,
            "icon": "eye-fill",
            "extra": {
                "id": "plone-smartweb-help-menu-rtfm",
                "separator": None,
                "class": "",
            },
            "submenu": None,
        }

        support = {
            "title": _("Ask a question"),
            "description": "",
            "action": support_action,
            "selected": False,
            "icon": "chat-square-heart-fill",
            "extra": {
                "id": "plone-smartweb-help-menu-support",
                "separator": None,
                "class": "",
            },
            "submenu": None,
        }

        workshop = {
            "title": _("Take part of workshop"),
            "description": "",
            "action": workshop_action,
            "selected": False,
            "icon": "rocket-takeoff-fill",
            "extra": {
                "id": "plone-smartweb-help-menu-workshop",
                "separator": None,
                "class": "",
            },
            "submenu": None,
        }

        menu_items = [rtfm, support, workshop]
        return menu_items
