# -*- coding: utf-8 -*-

from imio.smartweb.core.taxonomies.utils import add_page_taxonomy
from imio.smartweb.core.taxonomies.utils import add_procedure_taxonomy
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide unwanted profiles from site-creation and quickinstaller."""
        return [
            "imio.smartweb.core:testing",
            "imio.smartweb.core:uninstall",
        ]


def post_install(context):
    """Post install script"""
    add_page_taxonomy()
    add_procedure_taxonomy()


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
