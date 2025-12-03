# -*- coding: utf-8 -*-

from imio.smartweb.core.behaviors.subsite import IImioSmartwebSubsite
from imio.smartweb.core.contents import IFolder
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from plone.app.layout.navigation.interfaces import INavigationRoot
from Products.CMFPlone.interfaces.constrains import DISABLED
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from Products.Five.browser import BrowserView
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides


class CreateContentsForMigration(BrowserView):

    def __call__(self):
        # Faut lancer la migration depuis /Plone
        alsoProvides(self.request, IDisableCSRFProtection)
        self.create_content("actualites", "Actualités")
        self.create_content("images", "Images")

    def create_content(self, id, title):
        fr = [obj for obj in self.context.items() if obj[0] == "fr"][0][1]
        if id not in [i[0] for i in fr.items()]:
            api.content.create(
                id=id, title=title, container=fr, type="imio.smartweb.Folder"
            )
