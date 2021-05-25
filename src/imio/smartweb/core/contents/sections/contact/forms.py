# -*- coding: utf-8 -*-

from imio.smartweb.core.browser.forms import CustomAddForm
from imio.smartweb.core.browser.forms import CustomEditForm
from plone.dexterity.browser.add import DefaultAddView
from plone.z3cform import layout
from z3c.form.interfaces import HIDDEN_MODE


class ContactCustomAddForm(CustomAddForm):
    portal_type = "imio.smartweb.SectionContact"

    def updateFields(self):
        super(CustomAddForm, self).updateFields()
        if "hide_title" in self.fields:
            self.fields["hide_title"].field.default = True
            # We hide field that hide title because we want nobody can change the default value for contact (default = True)
            self.fields["hide_title"].mode = HIDDEN_MODE


class ContactCustomAddView(DefaultAddView):
    form = ContactCustomAddForm


class ContactCustomEditForm(CustomEditForm):
    def updateFields(self):
        super(ContactCustomEditForm, self).updateFields()
        if "hide_title" in self.fields:
            self.fields["hide_title"].field.default = True
            # We hide field that hide title because we want nobody can change the default value for contact (default = True)
            self.fields["hide_title"].mode = HIDDEN_MODE


ContactCustomEditView = layout.wrap_form(ContactCustomEditForm)
