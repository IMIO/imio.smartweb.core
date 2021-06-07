# -*- coding: utf-8 -*-

from imio.smartweb.core.contents import IDefaultPages
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.browser.add import DefaultAddView
from plone.dexterity.browser.edit import DefaultEditForm
from plone.z3cform import layout
from z3c.form.interfaces import DISPLAY_MODE
from z3c.form.interfaces import HIDDEN_MODE


class CustomAddForm(DefaultAddForm):
    css_class = "tabbed-form-with-toggle"
    enable_form_tabbing = False

    def updateFields(self):
        super(CustomAddForm, self).updateFields()
        if "ILeadImageBehavior.image_caption" in self.fields:
            # We don't use leadimage caption anywhere
            self.fields["ILeadImageBehavior.image_caption"].mode = HIDDEN_MODE

    def updateWidgets(self):
        super(CustomAddForm, self).updateWidgets()
        self.widgets["IBasic.description"].description = _(
            u"Use **text** to set text in bold and *text* to set text in italic."
        )


class CustomAddView(DefaultAddView):
    form = CustomAddForm


class CustomEditForm(DefaultEditForm):
    css_class = "tabbed-form-with-toggle"
    enable_form_tabbing = False

    def updateFields(self):
        super(CustomEditForm, self).updateFields()
        if "ILeadImageBehavior.image_caption" in self.fields:
            # We don't use leadimage caption anywhere
            self.fields["ILeadImageBehavior.image_caption"].mode = HIDDEN_MODE
        if IDefaultPages.providedBy(self.context):
            # We need to make exclude_from_nav field read only as it is used
            # for default pages to exclude them from sitemap / navigation / ...
            for group in self.groups:
                if "IExcludeFromNavigation.exclude_from_nav" in group.fields:
                    group.fields[
                        "IExcludeFromNavigation.exclude_from_nav"
                    ].mode = DISPLAY_MODE

    def updateWidgets(self):
        super(CustomEditForm, self).updateWidgets()
        self.widgets["IBasic.description"].description = _(
            u"Use **text** to set text in bold and *text* to set text in italic."
        )


CustomEditView = layout.wrap_form(CustomEditForm)
