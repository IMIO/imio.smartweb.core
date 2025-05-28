# -*- coding: utf-8 -*-

from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.autoform.directives import widget
from plone.z3cform import layout
from zope import schema
from z3c.form import field
from zope.interface import Interface


class IProcedureTextRowSchema(Interface):
    language = schema.TextLine(
        title=_("Language (en, fr,...)"),
        description=_("Enter the language code. Ex.: en"),
    )

    text = schema.TextLine(title=_("Text"), description=_("Your button title"))


class ISmartwebSiteAdminControlPanel(Interface):

    # directives.widget(
    #     "procedure_button_text", DataGridFieldFactory, allow_reorder=True, auto_append=False
    # )
    widget(procedure_button_text=DataGridFieldFactory)
    procedure_button_text = schema.List(
        title=_("Procedure : Define button text"),
        description=_("Choose procedure submission button text"),
        value_type=DictRow(
            title="Value",
            schema=IProcedureTextRowSchema,
        ),
        missing_value=[],
        min_length=1,
        required=True,
    )


class SmartwebSiteAdminControlPanelForm(RegistryEditForm):
    schema = ISmartwebSiteAdminControlPanel
    schema_prefix = "smartweb"
    label = _("Smartweb Site admin Settings")
    fields = field.Fields(ISmartwebSiteAdminControlPanel)


SmartwebSiteAdminControlPanelView = layout.wrap_form(
    SmartwebSiteAdminControlPanelForm, ControlPanelFormWrapper
)
