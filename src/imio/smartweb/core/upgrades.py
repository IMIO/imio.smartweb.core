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
