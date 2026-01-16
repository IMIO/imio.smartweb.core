# -*- coding: utf-8 -*-
from imio.smartweb.common.ia.browser.categorization_button_edit import (
    IACategorizeEditForm,
)
from imio.smartweb.core.browser.forms import SmartwebCustomEditForm
from plone.z3cform import layout
from z3c.form.interfaces import HIDDEN_MODE


FIELD_NAME = "categorization_ia_link"  # Internal id for dummy field


class PageEditForm(SmartwebCustomEditForm, IACategorizeEditForm):
    """Vue edit custom, avec bouton 'Catégoriser' injecté en haut de 'categorization'."""

    def update(self):
        # Hide hide_title in 'layout' group
        for group in getattr(self, "groups", []):
            if (
                getattr(group, "__name__", "") == "layout"
                and "hide_title" in group.widgets
            ):
                group.widgets["hide_title"].mode = HIDDEN_MODE
                group.widgets["hide_title"].value = ["selected"]
        super(PageEditForm, self).update()


PageEditView = layout.wrap_form(PageEditForm)
