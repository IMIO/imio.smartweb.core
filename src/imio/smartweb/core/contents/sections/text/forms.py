# -*- coding: utf-8 -*-

from imio.smartweb.core.browser.forms import SmartwebCustomAddForm
from imio.smartweb.core.browser.forms import SmartwebCustomEditForm
from plone.dexterity.browser.add import DefaultAddView
from plone.z3cform import layout
from z3c.form.interfaces import HIDDEN_MODE


class TextCustomAddForm(SmartwebCustomAddForm):
    portal_type = "imio.smartweb.SectionText"

    def update(self):
        super(TextCustomAddForm, self).update()
        # We hide hide_title field so no one can change the value for text
        # and set True value (single checkbox)
        for group in self.groups:
            if group.__name__ == "layout":
                group.widgets["hide_title"].mode = HIDDEN_MODE
                group.widgets["hide_title"].value = ["selected"]


class TextCustomAddView(DefaultAddView):
    form = TextCustomAddForm


class TextCustomEditForm(SmartwebCustomEditForm):
    def update(self):
        super(TextCustomEditForm, self).update()
        # We hide hide_title field so no one can change the value for text
        # and set True value (single checkbox)
        for group in self.groups:
            if group.__name__ == "layout":
                group.widgets["hide_title"].mode = HIDDEN_MODE
                group.widgets["hide_title"].value = ["selected"]


TextCustomEditView = layout.wrap_form(TextCustomEditForm)
