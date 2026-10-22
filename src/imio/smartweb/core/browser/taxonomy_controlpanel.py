# -*- coding: utf-8 -*-

from collective.taxonomy.controlpanel import TaxonomySettingsControlPanelForm
from collective.taxonomy.jsonimpl import ImportJson
from imio.smartweb.core.utils import reindexing_changed_terms
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


class SmartwebImportJson(ImportJson):
    """Save the terms of a taxonomy, then reindex the objects whose term
    labels changed (see indexers.SmartwebIndexableObjectWrapper)."""

    def __call__(self):
        with reindexing_changed_terms():
            return super().__call__()
