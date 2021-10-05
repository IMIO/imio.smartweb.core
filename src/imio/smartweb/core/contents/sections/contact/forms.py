# -*- coding: utf-8 -*-

from imio.smartweb.common.browser.forms import CustomAddForm
from imio.smartweb.core.browser.forms import SmartwebCustomEditForm
from plone.dexterity.browser.add import DefaultAddView
from plone.z3cform import layout
from z3c.form.interfaces import HIDDEN_MODE


class ContactCustomAddForm(CustomAddForm):
    portal_type = "imio.smartweb.SectionContact"

    def update(self):
        super(ContactCustomAddForm, self).update()
        # We hide hide_title field so no one can change the value for contact
        # and set True value (single checkbox)
        for group in self.groups:
            if group.__name__ == "layout":
                group.widgets["hide_title"].mode = HIDDEN_MODE
                group.widgets["hide_title"].value = ["selected"]


class ContactCustomAddView(DefaultAddView):
    form = ContactCustomAddForm


class ContactCustomEditForm(SmartwebCustomEditForm):
    def update(self):
        super(ContactCustomEditForm, self).update()
        # We hide hide_title field so no one can change the value for contact
        # and set True value (single checkbox)
        for group in self.groups:
            if group.__name__ == "layout":
                group.widgets["hide_title"].mode = HIDDEN_MODE
                group.widgets["hide_title"].value = ["selected"]


ContactCustomEditView = layout.wrap_form(ContactCustomEditForm)
