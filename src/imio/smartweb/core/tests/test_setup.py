# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles, TEST_USER_ID

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that imio.smartweb.core is properly installed."""

    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")

    def test_product_installed(self):
        """Test if imio.smartweb.core is installed."""
        self.assertTrue(self.installer.isProductInstalled("imio.smartweb.core"))

    def test_browserlayer(self):
        """Test that IImioSmartwebCoreLayer is registered."""
        from imio.smartweb.core.interfaces import IImioSmartwebCoreLayer
        from plone.browserlayer import utils

        self.assertIn(IImioSmartwebCoreLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstallProducts(["imio.smartweb.core"])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if imio.smartweb.core is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled("imio.smartweb.core"))

    def test_browserlayer_removed(self):
        """Test that IImioSmartwebCoreLayer is removed."""
        from imio.smartweb.core.interfaces import IImioSmartwebCoreLayer
        from plone.browserlayer import utils

        self.assertNotIn(IImioSmartwebCoreLayer, utils.registered_layers())
