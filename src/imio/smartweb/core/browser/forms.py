# -*- coding: utf-8 -*-

from imio.smartweb.common.browser.forms import CustomAddForm
from imio.smartweb.common.browser.forms import CustomEditForm
from imio.smartweb.core.behaviors.minisite import IImioSmartwebMinisite
from imio.smartweb.core.contents import IDefaultPages
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.dexterity.browser.add import DefaultAddView
from plone.z3cform import layout
from z3c.form.interfaces import DISPLAY_MODE


class SmartwebCustomAddForm(CustomAddForm):
    def updateWidgets(self):
        super(SmartwebCustomAddForm, self).updateWidgets()
        if "IBasic.description" in self.widgets:
            self.widgets["IBasic.description"].description = _(
                u"Use **text** to set text in bold and *text* to set text in italic."
            )


class SmartwebCustomAddView(DefaultAddView):
    form = SmartwebCustomAddForm


class SmartwebCustomEditForm(CustomEditForm):
    def updateFields(self):
        super(SmartwebCustomEditForm, self).updateFields()
        if IDefaultPages.providedBy(self.context) or IImioSmartwebMinisite.providedBy(
            self.context
        ):
            # We need to make exclude_from_nav field read only as it is used
            # for default pages to exclude them from sitemap / navigation / ...
            # and for minisites to exclude them as well.
            for group in self.groups:
                if "IExcludeFromNavigation.exclude_from_nav" in group.fields:
                    group.fields[
                        "IExcludeFromNavigation.exclude_from_nav"
                    ].mode = DISPLAY_MODE

    def updateWidgets(self):
        super(SmartwebCustomEditForm, self).updateWidgets()
        if "IBasic.description" in self.widgets:
            self.widgets["IBasic.description"].description = _(
                u"Use **text** to set text in bold and *text* to set text in italic."
            )


SmartwebCustomEditView = layout.wrap_form(SmartwebCustomEditForm)
