# -*- coding: utf-8 -*-

from imio.smartweb.common.browser.forms import CustomAddForm
from imio.smartweb.common.widgets.select import TranslatedAjaxSelectWidget
from imio.smartweb.core.browser.forms import SmartwebCustomEditForm
from imio.smartweb.core.contents.sections.contact.utils import build_display_rows
from imio.smartweb.core.contents.sections.contact.utils import CONTACT_ROW_COLUMNS
from imio.smartweb.core.contents.sections.contact.utils import CONTACT_ROW_KEYS
from imio.smartweb.core.contents.sections.contact.utils import get_remote_contacts
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from plone.dexterity.browser.add import DefaultAddView
from plone.z3cform import layout
from z3c.form import button
from z3c.form.interfaces import HIDDEN_MODE

DISPLAY_FIELDS = ("phones_display", "mails_display", "urls_display")

# related_contacts is an AjaxSelectWidget: it submits ONE text input holding
# every selected UID joined by this separator, not a list. Reading the raw
# request value would build a single bogus "uid1;uid2" UID.
RELATED_CONTACTS_SEPARATOR = TranslatedAjaxSelectWidget.separator

KIND_BY_FIELD = {
    "phones_display": "phones",
    "mails_display": "mails",
    "urls_display": "urls",
}


class ContactInformationsGridMixin:
    """Contact-form specifics: the informations grids and the hidden hide_title.

    Repopulates the read-only contact-informations grids from the directory.
    The grids are never "filled once": they are derived from the currently
    selected related_contacts. Rather than rebuilding widgets, this rewrites
    the request BEFORE super().update(), so the normal request -> widget path
    regenerates names, ids, the .count marker and the patterns by construction.

    It also hides the `hide_title` field after the widgets exist, which both
    concrete forms need and neither may forget.
    """

    def update(self):
        if self.request.form.get(self._load_button_name):
            self._reload_display_grids()
        super().update()
        self._hide_hide_title()

    @property
    def _load_button_name(self):
        return "{}buttons.load_contact_informations".format(self.prefix)

    def _reload_display_grids(self):
        uids = self._submitted_contact_uids()
        if not uids:
            api.portal.show_message(
                _("Please select a contact before loading its information."),
                request=self.request,
                type="info",
            )
            contacts = []
        else:
            contacts = get_remote_contacts(uids)
            if not contacts:
                # get_remote_contacts returns [] for a timeout, a non-200 and
                # an unreachable host alike (utils.get_json swallows every
                # exception), so "UIDs submitted but nothing came back" can
                # only be a failure. Rewriting the grids here would empty them
                # and destroy every recorded visible_columns preference on the
                # next save, so leave the request untouched.
                api.portal.show_message(
                    _(
                        "The contact directory could not be reached: contact "
                        "information was not loaded and nothing was changed."
                    ),
                    request=self.request,
                    type="error",
                )
                return
            api.portal.show_message(
                _("Contact information has been loaded."),
                request=self.request,
                type="info",
            )
        for field_name in DISPLAY_FIELDS:
            kind = KIND_BY_FIELD[field_name]
            prefix = "{}widgets.{}".format(self.prefix, field_name)
            preferences = self._extract_preferences(prefix, kind)
            rows = build_display_rows(kind, contacts, preferences)
            self._write_grid(prefix, kind, rows)

    def _submitted_contact_uids(self):
        """UIDs currently selected in related_contacts, in order.

        The AjaxSelectWidget submits them as a single separator-joined string;
        a plain list is accepted too so the method does not depend on the
        widget in use.
        """
        uids = self.request.form.get("{}widgets.related_contacts".format(self.prefix))
        if isinstance(uids, str):
            uids = uids.split(RELATED_CONTACTS_SEPARATOR)
        return [uid.strip() for uid in uids or [] if uid and uid.strip()]

    def _extract_preferences(self, prefix, kind):
        """Checkbox state already in the request, keyed (contact_uid, row_key).

        A row whose checkbox group submitted nothing yields an EMPTY list --
        "explicitly hidden" -- not a missing key. The widget was rendered (we
        only look at indices whose contact_uid is present), so "nothing
        submitted" can only mean "everything unchecked".
        """
        form = self.request.form
        key_column = CONTACT_ROW_KEYS[kind]
        preferences = {}
        index = 0
        while "{}.{}.widgets.contact_uid".format(prefix, index) in form:
            row_prefix = "{}.{}.widgets".format(prefix, index)
            key = (form.get("{}.{}".format(row_prefix, key_column)) or "").strip()
            if key:
                columns = form.get("{}.visible_columns".format(row_prefix))
                if columns is None:
                    columns = []
                elif isinstance(columns, str):
                    columns = [columns]
                uid = form.get("{}.contact_uid".format(row_prefix)) or ""
                preferences[(uid, key)] = list(columns)
            index += 1
        return preferences

    def _write_grid(self, prefix, kind, rows):
        form = self.request.form
        for key in [key for key in form if key.startswith("{}.".format(prefix))]:
            del form[key]
        columns = ("contact_uid", "contact_title") + CONTACT_ROW_COLUMNS[kind]
        for index, row in enumerate(rows):
            row_prefix = "{}.{}.widgets".format(prefix, index)
            for column in columns:
                form["{}.{}".format(row_prefix, column)] = row.get(column) or ""
            form["{}.visible_columns".format(row_prefix)] = list(row["visible_columns"])
            form["{}.visible_columns-empty-marker".format(row_prefix)] = "1"
        form["{}.count".format(prefix)] = str(len(rows))

    def _hide_hide_title(self):
        # We hide hide_title field so no one can change the value for contact
        # and set True value (single checkbox)
        for group in self.groups:
            if group.__name__ == "layout":
                group.widgets["hide_title"].mode = HIDDEN_MODE
                group.widgets["hide_title"].value = ["selected"]


class ContactCustomAddForm(ContactInformationsGridMixin, CustomAddForm):
    portal_type = "imio.smartweb.SectionContact"

    # Both MUST be copied before the decorator runs: @buttonAndHandler does a
    # setdefault on the `buttons` AND on the `handlers` name of the class body
    # being defined. Without the copies it would create fresh, empty managers
    # that shadow the base ones -- the form would lose the Save / Cancel
    # buttons (buttons) and, more silently, their handlers (handlers), so
    # pressing Save would render the form again without saving anything.
    buttons = CustomAddForm.buttons.copy()
    handlers = CustomAddForm.handlers.copy()

    @button.buttonAndHandler(
        _("Load contact information"), name="load_contact_informations"
    )
    def handleLoadContactInformations(self, action):
        """No-op: the grids were already rebuilt in update()."""


class ContactCustomAddView(DefaultAddView):
    form = ContactCustomAddForm


class ContactCustomEditForm(ContactInformationsGridMixin, SmartwebCustomEditForm):
    # See ContactCustomAddForm for why both managers are copied here.
    buttons = SmartwebCustomEditForm.buttons.copy()
    handlers = SmartwebCustomEditForm.handlers.copy()

    @button.buttonAndHandler(
        _("Load contact information"), name="load_contact_informations"
    )
    def handleLoadContactInformations(self, action):
        """No-op: the grids were already rebuilt in update()."""


ContactCustomEditView = layout.wrap_form(ContactCustomEditForm)
