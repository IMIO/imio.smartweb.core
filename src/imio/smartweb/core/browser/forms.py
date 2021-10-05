# -*- coding: utf-8 -*-

from imio.smartweb.common.browser.forms import CustomEditForm
from imio.smartweb.core.behaviors.minisite import IImioSmartwebMinisite
from imio.smartweb.core.contents import IDefaultPages
from plone.z3cform import layout
from z3c.form.interfaces import DISPLAY_MODE


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


SmartwebCustomEditView = layout.wrap_form(SmartwebCustomEditForm)
