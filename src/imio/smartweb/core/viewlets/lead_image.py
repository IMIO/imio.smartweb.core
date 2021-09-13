# -*- coding: utf-8 -*-

from plone.app.contenttypes.behaviors.viewlets import LeadImageViewlet


class NoLeadImageViewlet(LeadImageViewlet):
    """Leadimage viewlet that will be unavailable for pages & folders"""

    def update(self):
        super(NoLeadImageViewlet, self).update()
        self.available = False
