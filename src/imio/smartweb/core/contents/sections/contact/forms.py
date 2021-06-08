# -*- coding: utf-8 -*-

from imio.smartweb.core.browser.forms import CustomAddForm
from imio.smartweb.core.browser.forms import CustomEditForm
from plone.dexterity.browser.add import DefaultAddView
from plone.z3cform import layout
from z3c.form.interfaces import HIDDEN_MODE


class ContactCustomAddForm(CustomAddForm):
    portal_type = "imio.smartweb.SectionContact"

    def updateWidgets(self):
        super(ContactCustomAddForm, self).updateWidgets()
        # We hide hide_title field so no one can change the value for contact
        # and set True value (single checkbox)
        self.widgets["hide_title"].mode = HIDDEN_MODE
        self.widgets["hide_title"].value = ["selected"]


class ContactCustomAddView(DefaultAddView):
    form = ContactCustomAddForm


class ContactCustomEditForm(CustomEditForm):
    def updateWidgets(self):
        super(ContactCustomEditForm, self).updateWidgets()
        # We hide hide_title field so no one can change the value for contact
        # and set True value (single checkbox)
        self.widgets["hide_title"].mode = HIDDEN_MODE
        self.widgets["hide_title"].value = ["selected"]


ContactCustomEditView = layout.wrap_form(ContactCustomEditForm)
