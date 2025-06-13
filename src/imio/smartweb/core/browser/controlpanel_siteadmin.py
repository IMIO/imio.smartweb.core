# -*- coding: utf-8 -*-

from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.autoform.directives import omitted
from plone.autoform.directives import mode
from plone.autoform.directives import widget
from plone.registry.interfaces import IRegistry
from plone.z3cform import layout
from Products.statusmessages.interfaces import IStatusMessage

from z3c.form.interfaces import ActionExecutionError
from zope import schema
from zope.component import getUtility
from zope.interface import Interface
from zope.interface import Invalid
from zope.schema import ValidationError
from zope import schema

import json
import logging

logger = logging.getLogger("imio.smartweb.core.browser.controlpanel_siteadmin")

MAX_LENGTH = 33


class LabelTooLong(ValidationError):
    __doc__ = f"Le texte ne peut pas dépasser {MAX_LENGTH} caractères."


def max_length_constraint(value):
    if len(value) > MAX_LENGTH:
        raise LabelTooLong(value)
    return True


class IProcedureTextRowSchema(Interface):

    omitted("label_id")
    mode(label_id="hidden")
    label_id = schema.TextLine(
        title=_("ID"),
        description=_("Unique identifier for the procedure button text"),
        required=False,
    )
    label_fr = schema.TextLine(
        title=_("Label (fr)"),
        description=_("Your button title (french)"),
        constraint=max_length_constraint,
        required=True,
    )
    label_nl = schema.TextLine(
        title=_("Label (nl)"),
        description=_("Your button title (dutch)"),
        constraint=max_length_constraint,
        required=False,
    )
    label_de = schema.TextLine(
        title=_("Label (de)"),
        description=_("Your button title (german)"),
        constraint=max_length_constraint,
        required=False,
    )
    label_en = schema.TextLine(
        title=_("Label (en)"),
        description=_("Your button title (english)"),
        constraint=max_length_constraint,
        required=False,
    )


class ISmartwebSiteAdminControlPanel(Interface):

    widget(procedure_button_text=DataGridFieldFactory)
    procedure_button_text = schema.List(
        title=_("Procedure : Define button text"),
        description=_("Choose procedure submission button text"),
        value_type=DictRow(
            title="Labels",
            schema=IProcedureTextRowSchema,
        ),
        default=[],
        required=False,
    )


class SmartwebSiteAdminControlPanelForm(RegistryEditForm):
    schema = ISmartwebSiteAdminControlPanel
    schema_prefix = "smartweb"
    label = _("Smartweb Site admin Settings")
    # fields = field.Fields(ISmartwebSiteAdminControlPanel)


class SmartwebSiteAdminControlPanelForm(RegistryEditForm):
    schema = ISmartwebSiteAdminControlPanel
    schema_prefix = "smartweb"
    label = _("Smartweb Site admin Settings")

    def applyChanges(self, data):
        rows = data.get("procedure_button_text") or []
        for row in rows:
            all_label_ids = [row.get("label_id") for row in rows if row.get("label_id")]
            numbers = [
                int(label.split("-")[1])
                for label in all_label_ids
                if isinstance(label, str)
                and label.startswith("label-")
                and label.split("-")[1].isdigit()
            ]
            max_number = max(numbers, default=0)
            if row.get("label_id") is None:
                max_number += 1
                row["label_id"] = f"label-{max_number}"
        new_ids = {row.get("label_id") for row in rows if row.get("label_id")}

        registry = getUtility(IRegistry)
        old_rows = registry.get("smartweb.procedure_button_text") or []
        old_ids = {row.get("label_id") for row in old_rows if row.get("label_id")}

        removed_ids = old_ids - new_ids
        if removed_ids:
            brains = api.content.find(portal_type="imio.smartweb.Procedure")
            for removed_id in removed_ids:
                for brain in brains:
                    obj = brain.getObject()
                    if obj.button_ts_label == removed_id:
                        IStatusMessage(self.request).addStatusMessage(
                            f"Label ID '{removed_id}' is still used in Procedure '{obj.absolute_url()}' and will not be removed.",
                            type="error",
                        )
                        return False
        return super().applyChanges(data)


SmartwebSiteAdminControlPanelView = layout.wrap_form(
    SmartwebSiteAdminControlPanelForm, ControlPanelFormWrapper
)
