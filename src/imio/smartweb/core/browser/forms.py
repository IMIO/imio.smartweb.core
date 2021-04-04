# -*- coding: utf-8 -*-

from imio.smartweb.core.contents import IDefaultPages
from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.browser.add import DefaultAddView
from plone.dexterity.browser.edit import DefaultEditForm
from plone.z3cform import layout
from z3c.form.interfaces import DISPLAY_MODE


class CustomAddForm(DefaultAddForm):
    css_class = "tabbed-form-with-toggle"
    enable_form_tabbing = False


class CustomAddView(DefaultAddView):
    form = CustomAddForm


class CustomEditForm(DefaultEditForm):
    css_class = "tabbed-form-with-toggle"
    enable_form_tabbing = False

    def updateFields(self):
        super(DefaultEditForm, self).updateFields()

        if IDefaultPages.providedBy(self.context):
            # We need to make exclude_from_nav field read only as it is used
            # for default pages to exclude them from sitemap / navigation / ...
            for group in self.groups:
                if "IExcludeFromNavigation.exclude_from_nav" in group.fields:
                    group.fields[
                        "IExcludeFromNavigation.exclude_from_nav"
                    ].mode = DISPLAY_MODE


CustomEditView = layout.wrap_form(CustomEditForm)
