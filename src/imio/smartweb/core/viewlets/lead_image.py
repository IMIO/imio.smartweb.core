# -*- coding: utf-8 -*-

from plone.app.contenttypes.behaviors.viewlets import LeadImageViewlet


class PagesLeadImageViewlet(LeadImageViewlet):
    """Leadimage viewlet that will be unavailable for pages"""

    def update(self):
        super(PagesLeadImageViewlet, self).update()
        self.available = False
