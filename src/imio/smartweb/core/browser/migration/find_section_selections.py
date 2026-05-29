# -*- coding: utf-8 -*-

from plone import api
from Products.Five.browser import BrowserView
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides


class FindSectionSelectionsView(BrowserView):

    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        self.completed = []
        self.uncompleted = []

        brains = api.content.find(portal_type="imio.smartweb.SectionSelections")
        for brain in brains:
            obj = brain.getObject()
            selected_items = getattr(obj, "selected_items", None) or []
            if not selected_items or any(
                rel.to_object is None for rel in selected_items
            ):
                self.uncompleted.append(obj.absolute_url())
            else:
                self.completed.append(obj.absolute_url())

        return self.index()
