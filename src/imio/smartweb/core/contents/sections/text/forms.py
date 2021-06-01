# -*- coding: utf-8 -*-

from imio.smartweb.core.browser.forms import CustomAddForm
from imio.smartweb.core.browser.forms import CustomEditForm
from plone.dexterity.browser.add import DefaultAddView
from plone.z3cform import layout
from z3c.form.interfaces import HIDDEN_MODE


class TextCustomAddForm(CustomAddForm):
    portal_type = "imio.smartweb.SectionText"

    def updateFields(self):
        super(CustomAddForm, self).updateFields()
        # We hide hide_title field so no one can change the value for text
        self.fields["hide_title"].mode = HIDDEN_MODE

    def updateWidgets(self):
        super(CustomAddForm, self).updateWidgets()
        # We set True value for hide_title widget (single checkbox) for text
        self.widgets["hide_title"].value = ["selected"]


class TextCustomAddView(DefaultAddView):
    form = TextCustomAddForm


class TextCustomEditForm(CustomEditForm):
    def updateFields(self):
        super(TextCustomEditForm, self).updateFields()
        # We hide hide_title field so no one can change the value for text
        self.fields["hide_title"].mode = HIDDEN_MODE

    def updateWidgets(self):
        super(TextCustomEditForm, self).updateWidgets()
        # We set True value for hide_title widget (single checkbox) for text
        self.widgets["hide_title"].value = ["selected"]


TextCustomEditView = layout.wrap_form(TextCustomEditForm)
