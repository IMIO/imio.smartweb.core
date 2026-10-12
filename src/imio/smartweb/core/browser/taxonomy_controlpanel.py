# -*- coding: utf-8 -*-

from collective.taxonomy.controlpanel import TaxonomySettingsControlPanelForm
from plone import api
from plone.app.registry.browser import controlpanel


class SmartwebTaxonomySettingsControlPanelForm(TaxonomySettingsControlPanelForm):
    """Taxonomy control panel where deleting a taxonomy is a restricted action."""

    def updateActions(self):
        super().updateActions()
        if not api.user.has_permission(
            "imio.smartweb.core: Delete taxonomy", obj=self.context
        ):
            # no action, no handler : the button can't be rendered nor submitted
            del self.actions["delete-taxonomy"]


class SmartwebTaxonomySettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = SmartwebTaxonomySettingsControlPanelForm
