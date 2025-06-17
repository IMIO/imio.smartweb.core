# -*- coding: utf-8 -*-

from imio.smartweb.core.utils import populate_procedure_button_text
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


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


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
