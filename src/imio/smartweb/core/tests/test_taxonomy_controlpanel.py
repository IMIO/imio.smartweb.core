# -*- coding: utf-8 -*-

from imio.smartweb.core.interfaces import IImioSmartwebCoreLayer
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter
from zope.interface import alsoProvides


class TestTaxonomySettingsControlPanelForm(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        alsoProvides(self.request, IImioSmartwebCoreLayer)

    def available_actions(self):
        view = getMultiAdapter((self.portal, self.request), name="taxonomy-settings")
        view.update()
        return list(view.form_instance.actions.keys())

    def test_update_actions(self):
        setRoles(self.portal, TEST_USER_ID, ["Site Administrator"])
        actions = self.available_actions()
        self.assertIn("add-taxonomy", actions)
        self.assertNotIn("delete-taxonomy", actions)

        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.assertIn("delete-taxonomy", self.available_actions())


# <audit>
#   <file>test_taxonomy_controlpanel.py</file>
#   <requirements_applied>R1, R2, R5, R6</requirements_applied>
#   <deviations>None</deviations>
#   <questions>None</questions>
# </audit>
