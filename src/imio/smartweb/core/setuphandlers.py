# -*- coding: utf-8 -*-

from imio.smartweb.core.utils import populate_procedure_button_text
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer

import logging

logger = logging.getLogger("imio.smartweb.core")
CAMPAIGNVIEW_PORTAL_TYPE = "imio.smartweb.CampaignView"


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide unwanted profiles from site-creation and quickinstaller."""
        return [
            "imio.smartweb.core:icons-basic",
            "imio.smartweb.core:icons-contenttypes",
            "imio.smartweb.core:last-compilation",
            "imio.smartweb.core:testing",
            "imio.smartweb.core:uninstall",
        ]

    def getNonInstallableProducts(self):
        """Hide unwanted products from site-creation and quickinstaller."""
        return [
            "imio.smartweb.core.upgrades",
        ]


def post_install(context):
    """Post install script"""
    populate_procedure_button_text()


def ideabox_uninstall(context):
    """Post uninstall script for the ideabox profile"""
    post_install(context)
    remove_campaignview_from_displayed_types()


def remove_campaignview_from_displayed_types():
    """Stop showing CampaignView in navigation once ideabox is uninstalled.

    plone.displayed_types is a site wide setting, so the element the ideabox
    profile appends to it has to be taken out by hand: GenericSetup can only
    append to (or purge) a registry collection, never remove a single element.
    """
    displayed_types = api.portal.get_registry_record("plone.displayed_types")
    if CAMPAIGNVIEW_PORTAL_TYPE not in displayed_types:
        return
    api.portal.set_registry_record(
        "plone.displayed_types",
        tuple(t for t in displayed_types if t != CAMPAIGNVIEW_PORTAL_TYPE),
    )
    logger.info(f"Removed {CAMPAIGNVIEW_PORTAL_TYPE} from plone.displayed_types")


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
