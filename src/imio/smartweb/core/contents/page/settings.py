# -*- coding: utf-8 -*-

from imio.smartweb.core.contents import IPage
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from Products.Five.browser import BrowserView


class PageSettings(BrowserView):
    """Page settings"""

    def transform_to_folder(self):
        """Moves a Page into a new Folder (with same id) displaying full view"""
        page = self.context
        container = self.context.aq_parent
        page_id = self.context.id
        page = api.content.rename(self.context, new_id="{}_MIGRATE".format(page_id))
        folder = api.content.create(
            container=container,
            type="imio.smartweb.Folder",
            id=page_id,
            title=page.title,
        )
        page = api.content.move(source=page, target=folder)
        api.content.rename(page, new_id=page_id)
        folder.setLayout("full_view")

        api.portal.show_message(
            _(u"Page has been successfully transformed into folder"), self.request
        )
        self.request.response.redirect(folder.absolute_url())

    @property
    def available(self):
        return IPage.providedBy(self.context)
