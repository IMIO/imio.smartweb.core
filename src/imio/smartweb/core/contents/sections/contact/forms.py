# -*- coding: utf-8 -*-

from imio.smartweb.common.browser.forms import CustomAddForm
from imio.smartweb.common.contact.forms import ContactInformationsGridMixin
from imio.smartweb.core.browser.forms import SmartwebCustomEditForm
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.dexterity.browser.add import DefaultAddView
from plone.z3cform import layout
from z3c.form import button
from z3c.form.interfaces import HIDDEN_MODE


class SectionContactGridMixin(ContactInformationsGridMixin):
    """The section's own bits: `related_contacts` and the hidden hide_title.

    The grid-reloading machinery itself lives in
    imio.smartweb.common.contact.forms, shared with imio.events.core.

    `hide_title` is hidden after the widgets exist, which both concrete forms
    need and neither may forget. It belongs to the Section base and does not
    exist outside one, which is why it is not in the shared mixin.
    """

    contact_uids_field = "related_contacts"

    def update(self):
        super().update()
        self._hide_hide_title()

    def _hide_hide_title(self):
        # We hide hide_title field so no one can change the value for contact
        # and set True value (single checkbox)
        for group in self.groups:
            if group.__name__ == "layout":
                group.widgets["hide_title"].mode = HIDDEN_MODE
                group.widgets["hide_title"].value = ["selected"]


class ContactCustomAddForm(SectionContactGridMixin, CustomAddForm):
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


class ContactCustomEditForm(SectionContactGridMixin, SmartwebCustomEditForm):
    # See ContactCustomAddForm for why both managers are copied here.
    buttons = SmartwebCustomEditForm.buttons.copy()
    handlers = SmartwebCustomEditForm.handlers.copy()

    @button.buttonAndHandler(
        _("Load contact information"), name="load_contact_informations"
    )
    def handleLoadContactInformations(self, action):
        """No-op: the grids were already rebuilt in update()."""


ContactCustomEditView = layout.wrap_form(ContactCustomEditForm)
