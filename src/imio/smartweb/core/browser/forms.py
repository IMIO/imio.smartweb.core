# -*- coding: utf-8 -*-

from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.browser.add import DefaultAddView
from plone.dexterity.browser.edit import DefaultEditForm
from plone.z3cform import layout


class CustomAddForm(DefaultAddForm):
    enable_form_tabbing = False


class CustomAddView(DefaultAddView):
    form = CustomAddForm


class CustomEditForm(DefaultEditForm):
    enable_form_tabbing = False


CustomEditView = layout.wrap_form(CustomEditForm)
