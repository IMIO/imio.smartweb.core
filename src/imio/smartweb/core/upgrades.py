# -*- coding: utf-8 -*-

from plone import api
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import logging

logger = logging.getLogger("imio.smartweb.core")
PROFILEID = "profile-imio.smartweb.core:default"


def configure_first_official_release(context):
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile(PROFILEID, "plone.app.registry")
    portal_setup.runImportStepFromProfile(PROFILEID, "typeinfo")

    portal_setup.runImportStepFromProfile(PROFILEID, "catalog")
    portal_catalog = api.portal.get_tool("portal_catalog")
    # we could index only imio.smartweb.Page contents, but for some reason
    # api.content.find() doesn't find all objects
    portal_catalog.clearFindAndRebuild()
    logger.info("Reindexed catalog for category_and_topics index / metadata")


def set_thumb_scales(context):
    api.portal.set_registry_record("plone.thumb_scale_listing", "liste")
    api.portal.set_registry_record("plone.thumb_scale_summary", "vignette")


def update_actions(context):
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile(PROFILEID, "actions")
    portal_actions = api.portal.get_tool("portal_actions")
    header_actions = getattr(portal_actions, "header_actions")
    if "e_guichet" in header_actions.objectIds():
        header_actions._delObject("e_guichet")
        logger.info("Deleted e_guichet header action")


def update_icons_and_names(context):
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile(
        "profile-imio.smartweb.core:icons-basic", "plone.app.registry"
    )
    registry = getUtility(IRegistry)
    for old_icon in [
        "annuaire",
        "demarches",
        "ecoles",
        "horaires",
        "mobilite",
        "parkings",
        "sports",
        "tourisme",
        "travaux",
    ]:
        if f"smartweb.icon.{old_icon}" in registry:
            del registry.records[f"smartweb.icon.{old_icon}"]


def reload_registry(context):
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile(PROFILEID, "plone.app.registry")


def reload_types(context):
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile(PROFILEID, "typeinfo")
