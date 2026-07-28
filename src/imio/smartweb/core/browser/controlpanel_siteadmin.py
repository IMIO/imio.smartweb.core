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
from z3c.form.browser.select import SelectWidget
from z3c.form.widget import FieldWidget

from zope import schema
from zope.component import getUtility
from zope.i18n import translate
from zope.interface import Interface
from zope.schema import ValidationError
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from xml.sax.saxutils import escape
from xml.sax.saxutils import quoteattr

import logging

logger = logging.getLogger("imio.smartweb.core.browser.controlpanel_siteadmin")

MAX_LENGTH = 33


class LabelTooLong(ValidationError):
    __doc__ = f"Le texte ne peut pas dépasser {MAX_LENGTH} caractères."


def max_length_constraint(value):
    if len(value) > MAX_LENGTH:
        raise LabelTooLong(value)
    return True


MAX_SITEMAP_ITEMS = 50

SITEMAP_SOURCE_VOCABULARY = SimpleVocabulary(
    [
        SimpleTerm(
            "imio.smartweb.EventsView",
            "imio.smartweb.EventsView",
            _("Agenda — à venir"),
        ),
        SimpleTerm(
            "imio.smartweb.NewsView",
            "imio.smartweb.NewsView",
            _("Actualités — les plus récents"),
        ),
        SimpleTerm(
            "imio.smartweb.DirectoryView",
            "imio.smartweb.DirectoryView",
            _("Annuaire — les plus récents"),
        ),
    ]
)

SITEMAP_FILTER_VOCABULARY = SimpleVocabulary(
    [SimpleTerm("most_recent", "most_recent", _("Default sort"))]
)


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


class FrozenLabelSelectWidget(SelectWidget):
    """Render a Choice column as a read-only label while still submitting it.

    A plain ``mode="display"`` column looks right but is skipped during
    extraction, so DictRow rejects every row on save. This widget keeps the
    field in input mode (thus extracted normally) yet renders only the term
    title plus a hidden input carrying the token — a per-row "frozen label"
    that persists. It mirrors exactly what the standard select would submit
    (``<name>:list`` + ``<name>-empty-marker``).
    """

    def render(self):
        # The DataGrid sets the sub-widget value to the raw field value (a
        # single token string), while a stand-alone SelectWidget holds a
        # list/tuple of tokens. Handle both so the label is never a stray
        # character (self.value[0] on a string would render "i").
        value = self.value
        if isinstance(value, (list, tuple)):
            token = value[0] if value else ""
        elif isinstance(value, str):
            token = value
        else:
            token = ""
        try:
            title = translate(
                self.terms.getTermByToken(token).title, context=self.request
            )
        except (LookupError, AttributeError):
            title = token
        return (
            '<span class="dgf-frozen-label">{label}</span>'
            '<input type="hidden" name={name} value={token} />'
            '<input type="hidden" name={marker} value="1" />'
        ).format(
            label=escape(title or ""),
            name=quoteattr("{}:list".format(self.name)),
            token=quoteattr(token),
            marker=quoteattr("{}-empty-marker".format(self.name)),
        )


def FrozenLabelFieldWidget(field, request):
    return FieldWidget(field, FrozenLabelSelectWidget(request))


class ISitemapSourceRowSchema(Interface):

    # source_type stays an input field (extracted on save) but is rendered as
    # a read-only label via FrozenLabelFieldWidget. A mode="display" column is
    # NOT submitted, which makes DictRow reject every row ("could not process
    # the value" / "required").
    widget(source_type=FrozenLabelFieldWidget)
    source_type = schema.Choice(
        title=_("Source"),
        vocabulary=SITEMAP_SOURCE_VOCABULARY,
        required=False,
    )
    enabled = schema.Bool(
        title=_("Enabled"),
        default=True,
        required=False,
    )
    max_items = schema.Int(
        title=_("Maximum number of items"),
        min=1,
        max=MAX_SITEMAP_ITEMS,
        default=MAX_SITEMAP_ITEMS,
        required=True,
    )
    item_filter = schema.Choice(
        title=_("Filter"),
        vocabulary=SITEMAP_FILTER_VOCABULARY,
        default="most_recent",
        required=True,
    )


class ISmartwebSiteAdminControlPanel(Interface):

    menu_position_select = schema.Choice(
        title=_("Choice of menu position"),
        description=_("Choice comportment of the menu on scroll"),
        vocabulary=SimpleVocabulary(
            [
                SimpleTerm(
                    value="default", token="default", title=_("Default position")
                ),
                SimpleTerm(
                    value="sticky",
                    token="sticky",
                    title=_("Sticky (always visible on scroll)"),
                ),
                SimpleTerm(
                    value="sticky-on-top",
                    token="sticky-on-top",
                    title=_("Sticky 2 (visible on upward scroll only)"),
                ),
            ]
        ),
        required=True,
        default="default",
    )

    widget(sitemap_authentic_sources=DataGridFieldFactory)
    sitemap_authentic_sources = schema.List(
        title=_("Sitemap: authentic sources configuration"),
        description=_(
            "Per authentic source: include it in the sitemap, cap how many "
            "remote items are listed, and choose the ordering. Disabling or "
            "lowering the count reduces the sitemap size."
        ),
        value_type=DictRow(
            title="SitemapSource",
            schema=ISitemapSourceRowSchema,
        ),
        default=[
            {
                "source_type": "imio.smartweb.EventsView",
                "enabled": True,
                "max_items": 50,
                "item_filter": "most_recent",
            },
            {
                "source_type": "imio.smartweb.NewsView",
                "enabled": True,
                "max_items": 50,
                "item_filter": "most_recent",
            },
            {
                "source_type": "imio.smartweb.DirectoryView",
                "enabled": True,
                "max_items": 50,
                "item_filter": "most_recent",
            },
        ],
        required=False,
    )

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

    def updateWidgets(self, prefix=None):
        super().updateWidgets(prefix)
        # The sitemap sources grid has a fixed set of rows (one per authentic
        # source); the admin edits them but must not add/remove/append rows.
        sitemap_widget = self.widgets.get("sitemap_authentic_sources")
        if sitemap_widget is not None:
            sitemap_widget.allow_insert = False
            sitemap_widget.allow_delete = False
            sitemap_widget.auto_append = False

    def applyChanges(self, data):
        # Guard: the sitemap grid must list each authentic source exactly once
        # (source_type is editable to satisfy the widget, so we validate it).
        sitemap_rows = data.get("sitemap_authentic_sources")
        if sitemap_rows is not None:
            source_types = [row.get("source_type") for row in sitemap_rows]
            if sorted(source_types) != sorted(SITEMAP_SOURCE_VOCABULARY.by_value):
                IStatusMessage(self.request).addStatusMessage(
                    _(
                        "The sitemap configuration must list each authentic "
                        "source exactly once."
                    ),
                    type="error",
                )
                return False

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
