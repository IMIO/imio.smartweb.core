# -*- coding: utf-8 -*-
from plone.app.contenttypes.behaviors.viewlets import (
    LeadImageViewlet as BaseLeadImageViewlet,
)
from imio.smartweb.core.behaviors.page import IPageSections


class LeadImageViewlet(BaseLeadImageViewlet):
    def update(self):
        super(LeadImageViewlet, self).update()
        if (
            IPageSections.providedBy(self.context)
            and "leadimage" not in self.context.visible_sections
        ):
            self.available = False
