# -*- coding: utf-8 -*-

from plone import api
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
